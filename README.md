# Aplicação de Rastreio de Pedidos (API MCH Gestão)

## 📖 Sobre o Projeto

Esta é uma aplicação web intermediária construída em Python com o framework Flask. Sua principal função é fornecer uma interface simples para que usuários possam consultar o status de rastreio de seus pedidos.

A aplicação:
1.  Apresenta um campo para o usuário digitar o número do pedido.
2.  Conecta-se à API da **MCH Gestão** para buscar os dados de rastreio.
3.  Exibe os status do pedido em uma página web gerada dinamicamente.
4.  É projetada para ser hospedada na plataforma **Fly.io**.

---

## ✨ Funcionalidades

-   [x] Página inicial com formulário para consulta de pedido.
-   [x] Integração com a API de rastreio (`/api/v1/tracking`) da MCH Gestão.
-   [x] Exibição do histórico de status do pedido em formato de tabela.
-   [x] Tratamento de erros para pedidos não encontrados ou falhas de comunicação com a API.
-   [x] Roteamento limpo (ex: `/rastreio/12345`).

---

## 🛠️ Tecnologias Utilizadas

-   **Backend:** Python 3
-   **Framework:** Flask
-   **Comunicação API:** Requests
-   **Frontend:** HTML5 / CSS
-   **Hospedagem:** Fly.io
-   **Servidor WSGI:** Gunicorn (usado pelo Fly.io no deploy)

---

## 🚀 Começando

Siga estas instruções para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

Você vai precisar ter as seguintes ferramentas instaladas:
-   [Python 3.8+](https://www.python.org/downloads/)
-   `pip` (gerenciador de pacotes do Python)
-   `venv` (para criar ambientes virtuais)
-   [Fly.io CLI (flyctl)](https://fly.io/docs/hands-on/install-flyctl/) (para o deploy)

### Instalação Local

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/kritski/rastreio.git](https://github.com/kritski/rastreio.git)
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
    (Primeiro, crie o arquivo `requirements.txt` se ele não existir)
    ```bash
    pip freeze > requirements.txt
    ```
    (Depois, instale a partir dele)
    ```bash
    pip install -r requirements.txt
    ```

###
