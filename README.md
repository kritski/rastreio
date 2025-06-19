# Aplicação de Rastreio de Pedidos (API MCH Gestão)

## ⚠️ Status Atual do Projeto (Junho de 2025)

A aplicação está completamente desenvolvida, testada e implantada na plataforma Fly.io. O código-fonte implementa corretamente a lógica para consultar a API da MCH Gestão e exibir os resultados.

No entanto, a aplicação encontra-se atualmente **bloqueada e não funcional** devido a um problema externo de conectividade com a API de destino. Após um processo de depuração exaustivo, foi concluído que o domínio `app.mchgestao.com.br` não está a ser resolvido corretamente por diversas redes de nuvem (incluindo Fly.io e Postman Cloud Agent), impedindo qualquer conexão.

**O próximo passo é aguardar a resolução do problema de DNS pela equipa de suporte técnico da MCH Gestão.**

---

## 📖 Sobre o Projeto

Esta é uma aplicação web construída em Python com o framework Flask. A sua principal função é atuar como um **Backend-for-Frontend (BFF)**, fornecendo uma interface segura e simples para que clientes possam consultar o status de rastreio de seus pedidos.

A aplicação:
1.  Apresenta um formulário para o utilizador digitar o número do pedido.
2.  Conecta-se à API da MCH Gestão para buscar os dados de rastreio de forma segura, sem expor as chaves de API ao cliente.
3.  Exibe o histórico de status do pedido em uma página web gerada dinamicamente.
4.  É projetada para ser hospedada de forma eficiente na plataforma **Fly.io**.

---

## 🛠️ Tecnologias Utilizadas

-   **Backend:** Python 3
-   **Framework:** Flask
-   **Comunicação API:** Requests
-   **Frontend:** HTML5 / CSS (inline)
-   **Hospedagem:** Fly.io
-   **Servidor WSGI:** Gunicorn

---

## 🔬 Histórico de Depuração e Diagnóstico

Para chegar à conclusão sobre o problema externo, foram realizados os seguintes passos de diagnóstico:

-   **Verificação de Credenciais:** As chaves de API (`MCH_API_KEY_PROD` e `_TEST`) foram validadas e configuradas corretamente como "secrets" no Fly.io.
-   **Logging Detalhado:** Foi implementado um sistema de logging robusto no `app.py` para monitorizar cada etapa do fluxo da requisição.
-   **Teste de Conectividade Interna:** Através do `fly ssh console`, confirmou-se que a máquina virtual da aplicação no Fly.io não conseguia resolver o hostname da API (`NameResolutionError`), mesmo após tentar forçar o uso de DNS alternativos.
-   **Validação Externa com Postman:** Testes realizados com o Postman (usando tanto o Cloud Agent quanto o Desktop Agent) confirmaram que o erro de resolução de DNS (`ENOTFOUND`) também ocorria a partir de outra infraestrutura de nuvem.
-   **Diagnóstico Final:** A incapacidade de múltiplos sistemas (Fly.io, Postman Cloud) de resolver o domínio, enquanto o acesso por IP direto é bloqueado por segurança (`SSL Handshake Failure`), prova conclusivamente que o problema reside na configuração de DNS pública do domínio `app.mchgestao.com.br`.

---

## 🚀 Como Executar o Projeto

Siga estas instruções para configurar e executar o projeto.

### Pré-requisitos

-   [Python 3.8+](https://www.python.org/downloads/)
-   `pip` e `venv`
-   [Fly.io CLI (flyctl)](https://fly.io/docs/hands-on/install-flyctl/)

### Instalação Local

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/kritski/rastreio.git
    cd rastreio
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação localmente:**
    ```bash
    flask run
    ```
    A aplicação estará disponível em `http://127.0.0.1:5000`. (Nota: A conexão com a API externa não funcionará localmente se o problema de DNS persistir na sua rede).

### Deploy no Fly.io (Instruções para uma Instalação Limpa)

1.  **Crie um novo app no Fly.io:**
    ```bash
    fly launch
    ```
    -   Escolha um nome para o app (ex: `meu-rastreio`).
    -   Escolha uma região (ex: `gru` para São Paulo).
    -   **NÃO** adicione um banco de dados Postgres ou Redis.

2.  **Configure os Secrets:**
    Adicione sua chave de API de produção. Lembre-se de usar o nome do seu novo app no parâmetro `-a`.
    ```bash
    fly secrets set MCH_API_KEY_PROD="mch_api_M3yB4CXrH6DH71PufFdCJGJZ" -a nome-do-seu-app
    ```

3.  **Atribua um Endereço IP:**
    Este passo é crucial para resolver problemas de conectividade na rede do Fly.io.
    ```bash
    fly ips allocate-v4 -a nome-do-seu-app
    ```

4.  **Faça o Deploy:**
    ```bash
    fly deploy
    ```
    O Fly.io usará o `Dockerfile` e o `fly.toml` do repositório para construir e iniciar sua aplicação.

---

## 📂 Estrutura do Projeto

```
.
├── app.py              # Lógica principal da aplicação Flask
├── fly.toml            # Arquivo de configuração do Fly.io
├── Dockerfile          # Instruções para construir a imagem da aplicação
├── requirements.txt    # Lista de dependências Python
├── templates/
│   ├── index.html      # Página inicial com o formulário
│   ├── rastreio.html   # Página que exibe os dados do rastreio
│   └── erro.html       # Página para exibir mensagens de erro
└── README.md           # Este arquivo
