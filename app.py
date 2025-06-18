import os
import logging
from flask import Flask, render_template, request, redirect, url_for
import requests
import sys

# --- Configuração do Logging Detalhado ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

app = Flask(__name__)

logging.info("Aplicação iniciada com correção de IP.")

# --- INÍCIO DA CORREÇÃO FINAL DE IP/DNS ---
# Usamos o IP direto do servidor, pois o DNS do Fly.io está falhando.
# O cabeçalho 'Host' é essencial para que o servidor de destino saiba qual site atender.
MCH_API_URL = "https://172.67.135.132/api/v1/tracking" 
MCH_HOST_HEADER = "app.mchgestao.com.br"
# --- FIM DA CORREÇÃO FINAL DE IP/DNS ---

MCH_API_KEY = os.getenv("MCH_API_KEY_PROD")

@app.route('/')
def index():
    """Renderiza a página inicial com o formulário."""
    logging.info("Renderizando a página inicial (index.html).")
    return render_template('index.html')

@app.route('/rastrear', methods=['POST'])
def rastrear():
    """Recebe o número do pedido do formulário e redireciona."""
    numero_pedido = request.form.get('pedido')
    logging.info(f"Recebido formulário com o pedido: {numero_pedido}")
    if numero_pedido:
        logging.info(f"Redirecionando para a página de rastreio do pedido {numero_pedido}.")
        return redirect(url_for('pagina_rastreio', numero_pedido=numero_pedido))
    
    logging.warning("Formulário recebido sem número de pedido. Redirecionando para a página inicial.")
    return redirect(url_for('index'))

@app.route('/rastreio/<numero_pedido>')
def pagina_rastreio(numero_pedido):
    """
    Busca os dados de rastreio na API da MCH e exibe a página.
    """
    logging.info(f"Iniciando busca de rastreio para o pedido: {numero_pedido}")

    if not MCH_API_KEY:
        logging.error("ERRO CRÍTICO: A chave da API (MCH_API_KEY_PROD) não foi encontrada nos secrets.")
        return render_template('erro.html', mensagem="A chave da API não foi configurada no servidor.")

    # Adicionamos o cabeçalho 'Host' para que o servidor de destino funcione corretamente
    headers = {
        'Authorization': f'Bearer {MCH_API_KEY}',
        'Host': MCH_HOST_HEADER
    }
    payload = {'order_number': numero_pedido}

    logging.info(f"Preparando para enviar requisição POST para o IP: {MCH_API_URL}")
    logging.info(f"Payload: {payload} | Headers: {headers}")

    try:
        # Adicionamos 'verify=False' como último recurso caso o certificado SSL não corresponda ao IP.
        # Isto desativa a verificação de segurança do certificado.
        response = requests.post(MCH_API_URL, headers=headers, json=payload, timeout=15, verify=False)
        logging.info(f"Resposta recebida da API com status: {response.status_code}")
        response.raise_for_status()

        dados_rastreio = response.json()
        logging.info(f"Dados de rastreio recebidos com sucesso para o pedido {numero_pedido}.")
        
        return render_template('rastreio.html', eventos=dados_rastreio, pedido=numero_pedido)

    except requests.exceptions.HTTPError as e:
        logging.error(f"Erro HTTP da API para o pedido {numero_pedido}. Status: {e.response.status_code}. Resposta: {e.response.text}")
        if e.response.status_code == 404:
            return render_template('erro.html', mensagem=f"O pedido {numero_pedido} não foi encontrado.")
        return render_template('erro.html', mensagem=f"A API retornou um erro inesperado.")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"ERRO DE CONEXÃO ao tentar contatar a API para o pedido {numero_pedido}: {e}")
        return render_template('erro.html', mensagem="Não foi possível conectar ao serviço de rastreio. Por favor, tente novamente mais tarde.")

