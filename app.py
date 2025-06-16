import os
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URL da API e a chave (serão lidas das "secrets" do Fly.io)
# O endpoint específico para rastreio é /api/v1/tracking
MCH_API_URL = "https://app.mchgestao.com.br/api/v1/tracking" 
MCH_API_KEY = os.getenv("MCH_API_KEY_TEST") # Começaremos com a chave de teste

@app.route('/')
def index():
    """Renderiza a página inicial com o formulário."""
    return render_template('index.html')

@app.route('/rastrear', methods=['POST'])
def rastrear():
    """Recebe o número do pedido do formulário e redireciona."""
    numero_pedido = request.form.get('pedido')
    if numero_pedido:
        # Redireciona para uma URL "limpa", ex: /rastreio/12345
        return redirect(url_for('pagina_rastreio', numero_pedido=numero_pedido))
    return redirect(url_for('index'))

@app.route('/rastreio/<numero_pedido>')
def pagina_rastreio(numero_pedido):
    """
    Busca os dados de rastreio na API da MCH e exibe a página.
    """
    if not MCH_API_KEY:
        return render_template('erro.html', mensagem="A chave da API não foi configurada no servidor.")

    headers = {'Authorization': f'Bearer {MCH_API_KEY}'}
    # A API espera um corpo (body) na requisição com o número do pedido
    payload = {'order_number': numero_pedido}

    try:
        # Usamos requests.post() para enviar os dados
        response = requests.post(MCH_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Lança um erro para status HTTP 4xx ou 5xx

        dados_rastreio = response.json()
        
        # A API retorna uma lista de eventos, vamos passar para o template
        return render_template('rastreio.html', eventos=dados_rastreio, pedido=numero_pedido)

    except requests.exceptions.HTTPError as e:
        # Trata erros específicos da API (ex: pedido não encontrado)
        if e.response.status_code == 404:
            return render_template('erro.html', mensagem=f"O pedido {numero_pedido} não foi encontrado.")
        return render_template('erro.html', mensagem=f"Erro na API: {str(e)}")
    except requests.exceptions.RequestException as e:
        # Trata erros de conexão
        return render_template('erro.html', mensagem=f"Erro de conexão: {str(e)}")
