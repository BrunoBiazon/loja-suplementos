# Loja de Suplementos E-commerce

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

Uma plataforma completa de e-commerce focada no nicho de suplementação alimentar. O projeto foi desenvolvido com foco em escalabilidade, utilizando **Docker** para containerização e implantado em uma instância **EC2 na AWS**, com integração real de pagamentos via **Mercado Pago**.

---

## 🚀 Funcionalidades

* **Gestão de Produtos:** Catálogo completo com suporte a categorias, preços e controle de estoque.
* **Checkout Inteligente:** Integração com API do Mercado Pago para pagamentos via Cartão, Pix e Boleto.
* **Painel Administrativo:** Interface completa para gestão de produtos, pedidos, usuários.
* **Arquitetura Cloud:** Deploy automatizado em ambiente de nuvem.
* **Segurança:** Variáveis de ambiente protegidas e isolamento de processos via containers.

---

## Arquitetura e Deploy

* **Docker Hub:** A imagem da aplicação está versionada e disponível para pull.
* **PostgreSQL:** Banco de dados robusto rodando em container isolado.
* **AWS EC2:** Hospedagem em servidor Ubuntu na nuvem.
   - Tipo de instância: t3.micro.
* **Ngrok:** Túnel seguro com suporte a HTTPS para comunicação com webhooks de pagamento.
* **Persistência:** Uso de Docker Volumes para manter dados do banco e arquivos de mídia (fotos de produtos) seguros.

---

## Como foi configurado o servidor/rede:

A administração remota da infraestrutura e a configuração de rede do servidor EC2 foram realizadas utilizando o cliente **MobaXterm**. 

Para garantir a alta disponibilidade e a comunicação contínua com os webhooks de pagamento (Mesmo quando o acesso SSH é encerrado), a seguinte arquitetura de rede local foi aplicada:

1. **Acesso SSH:** Conexão segura estabelecida com o servidor Ubuntu na AWS utilizando chaves `.pem`.
2. **Processos em Background (`screen`):** Utilização da ferramenta de multiplexação de terminal `screen` do Linux. Garantindo que a aplicação não caia ao fechar o MobaXterm, inicialização automática.
3. **Túnel Ngrok Seguro:** Execução do **Ngrok** em segundo plano para expor portas específicas do servidor localmente, criando um túnel HTTPS seguro vital para receber os callbacks (Webhooks) de mudança de status de pagamento do Mercado Pago.

---
<br><br>

## 🛠️ Como Executar o Projeto
Caso queria ver o checkout de pagamento, será necessário configurar o mercado pago e colocar o token no .env .

### 💳 Configurando o Mercado Pago (API e Webhooks)

Para que o checkout e a atualização de status de pedidos funcionem, você precisa configurar as suas credenciais do Mercado Pago:

1. Acesse o [Painel de Desenvolvedores do Mercado Pago](https://www.mercadopago.com.br/developers/panel/applications).
2. Crie uma nova aplicação e copie o seu **Access Token** (pode ser as credenciais de Teste ou Produção).
3. Cole esse token no arquivo `.env` na variável `MP_ACCESS_TOKEN`.
4. **Configuração do Webhook (Para testes locais):**
   * Inicie o Ngrok apontando para a porta do projeto: `ngrok http 8000`
   * No painel do Mercado Pago, vá em **Notificações > Webhooks**.
   * Adicione a URL gerada pelo Ngrok seguida do endpoint da sua aplicação. Exemplo: 
     `https://sua-url-ngrok.ngrok-free.dev/caminho-do-seu-webhook/`
   * Selecione o evento **Pagamentos (`payment`)** e salve.

---

### ⚙️ Configuração (Variáveis de Ambiente)
Independentemente da forma que você escolher para rodar o projeto, será necessário criar um arquivo `.env` na raiz do diretório com as seguintes variáveis:

    DEBUG=True
    SECRET_KEY=sua_secret_key_aqui
    DB_NAME=LojaBD
    DB_USER=postgres
    DB_PASSWORD=admin
    DB_HOST=db
    DB_PORT=5432
    MP_ACCESS_TOKEN=seu_token_do_mercado_pago

---

Com o `.env` configurado, você pode testar a aplicação de duas maneiras: baixando a imagem já pronta do Docker Hub ou clonando o repositório para fazer o build local:

### Opção 1: Via Docker Hub (Testar rapidamente)

Nesta opção, você não precisa do código fonte, apenas do arquivo de orquestração.

1. Crie uma pasta vazia e adicione o seu arquivo `.env`.
2. Crie um arquivo `docker-compose.yml` e cole a configuração abaixo:

    version: '3.8'

    services:
      db:
        image: postgres:15
        environment:
          - POSTGRES_DB=LojaBD
          - POSTGRES_USER=postgres
          - POSTGRES_PASSWORD=admin
        volumes:
          - postgres_data:/var/lib/postgresql/data

      web:
        image: brunobiazon/loja-suplementos:latest
        ports:
          - "8000:8000"
        env_file: .env
        depends_on:
          - db
        volumes:
          - media_data:/app/media

    volumes:
      postgres_data:
      media_data:

3. Abra o terminal na pasta e execute:

    docker-compose up -d
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser

---

### Opção 2: Via Git 

Nesta opção, você terá acesso a todo o código fonte e construirá a imagem do zero na sua máquina.

1. Clone o repositório e acesse a pasta:

    git clone https://github.com/BrunoBiazon/NOME_DO_SEU_REPOSITORIO.git
    cd NOME_DO_SEU_REPOSITORIO

2. Crie o arquivo `.env` na raiz do projeto (conforme a seção de configuração).

3. Faça o build das imagens e suba os containers:

    docker-compose up -d --build
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser

---
## Acessando a aplicação

O modo como você acessa a loja depende do que deseja testar:

### 1. Navegação Padrão (Localhost) - Caso não queria configurar webbook mercado pago.
Para navegar pela loja, ver o layout e gerenciar o catálogo, acesse diretamente:
👉 **http://localhost:8000**
* **Painel Administrativo:** `http://localhost:8000/admin` (Use as credenciais do `createsuperuser`).

### 2. Teste de Pagamento Completo (Ngrok)
Para testar o fluxo de checkout e receber o retorno (Webhooks) do Mercado Pago mudando o status do pedido em tempo real, você **deve** acessar a loja através do túnel Ngrok:
1. Inicie o túnel no seu terminal: `ngrok http 8000`
2. Acesse a URL HTTPS gerada (Ex: `https://sua-url.ngrok-free.dev`).
3. Certifique-se de que essa URL está configurada no painel do Mercado Pago e no seu arquivo `.env` (se necessário).
---
