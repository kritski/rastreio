import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# URL da API e a chave (serão lidas das "secrets" do Fly.io)
MCH_API_URL = "https://app.mchgestao.com.br/api/v1/tracking"
MCH_API_KEY = os.getenv("MCH_API_KEY_PROD") # Usando a chave de produção

@app.route('/')
def index():
    """Renderiza a página inicial com o formulário."""
    return render_template('index.html')

@app.route('/rastrear', methods=['POST'])
def rastrear():
    """Recebe o número do pedido do formulário e redireciona."""
    numero_pedido = request.form.get('pedido')
    if numero_pedido:
        return redirect(url_for('pagina_rastreio', numero_pedido=numero_pedido))
    return redirect(url_for('index'))

@app.route('/rastreio/<numero_pedido>')
def pagina_rastreio(numero_pedido):
    """
    Busca os dados de rastreio na API da MCH e exibe a página.
    """
    if not MCH_API_KEY:
        # Lidar com o caso em que a chave não está configurada
        return render_template('erro.html', mensagem="A chave da API não foi configurada no servidor.")

    headers = {'Authorization': f'Bearer {MCH_API_KEY}'}
    payload = {'order_number': numero_pedido}

    try:
        response = requests.post(MCH_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status() # Lança um erro para status HTTP 4xx ou 5xx
        
        dados_rastreio = response.json()
        return render_template('rastreio.html', eventos=dados_rastreio, pedido=numero_pedido)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return render_template('erro.html', mensagem=f"O pedido {numero_pedido} não foi encontrado.")
        # Para outros erros HTTP (500, 503, etc.)
        return render_template('erro.html', mensagem="O serviço de rastreio está temporariamente indisponível.")
        
    except requests.exceptions.RequestException:
        # Para erros de conexão, timeout, etc.
        return render_template('erro.html', mensagem="Não foi possível conectar ao serviço de rastreio. Verifique sua conexão ou tente novamente mais tarde.")
