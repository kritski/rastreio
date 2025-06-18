import os
import logging
import sys
import socket
import requests
import requests.packages.urllib3.util.connection as urllib3_cn
from flask import Flask, render_template, request, redirect, url_for

# --- INÍCIO DA CORREÇÃO DE IPV4 ---
# Força o uso de IPv4 para resolver o problema de DNS em redes IPv6-first como a do Fly.io
def allowed_gai_family():
    return socket.AF_INET
urllib3_cn.allowed_gai_family = allowed_gai_family
# --- FIM DA CORREÇÃO DE IPV4 ---


# --- Configuração do Logging Detalhado ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

app = Flask(__name__)

logging.info("Aplicação iniciada.")

# URL da API e a chave (serão lidas das "secrets" do Fly.io)
MCH_API_URL = "https://app.mchgestao.com.br/api/v1/tracking" 
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

    headers = {'Authorization': f'Bearer {MCH_API_KEY}'}
    payload = {'order_number': numero_pedido}

    logging.info(f"Preparando para enviar requisição POST para: {MCH_API_URL}")
    logging.info(f"Payload da requisição: {payload}")

    try:
        response = requests.post(MCH_API_URL, headers=headers, json=payload, timeout=10)
        logging.info(f"Resposta recebida da API com status: {response.status_code}")
        response.raise_for_status()

        dados_rastreio = response.json()
        logging.info(f"Dados de rastreio recebidos com sucesso para o pedido {numero_pedido}.")
        
        return render_template('rastreio.html', eventos=dados_rastreio, pedido=numero_pedido)

    except requests.exceptions.HTTPError as e:
        logging.error(f"Erro HTTP da API para o pedido {numero_pedido}. Status: {e.response.status_code}. Resposta: {e.response.text}", exc_info=True)
        if e.response.status_code == 404:
            return render_template('erro.html', mensagem=f"O pedido {numero_pedido} não foi encontrado.")
        return render_template('erro.html', mensagem=f"A API retornou um erro inesperado.")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"ERRO DE CONEXÃO ao tentar contatar a API para o pedido {numero_pedido}.", exc_info=True)
        return render_template('erro.html', mensagem="Não foi possível conectar ao serviço de rastreio. Verifique sua conexão ou tente novamente mais tarde.")
```

### Próximos Passos (A Solução Final)

1.  **Atualize os dois arquivos** no seu computador: o `Dockerfile` e o `app.py`, com os conteúdos que eu forneci acima.
2.  **No seu terminal**, na pasta do projeto, envie as duas alterações para o GitHub.
    ```bash
    git add Dockerfile app.py
    git commit -m "Força uso de IPv4 na aplicação para corrigir erro de DNS"
    git push
    ```

Este novo deploy irá construir a aplicação com o `Dockerfile` limpo e executar o código Python que sabe como lidar com a rede do Fly.io. Estou muito confiante de que isso resolverá o problema de conexão de uma vez por tod