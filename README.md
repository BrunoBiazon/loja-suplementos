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
* **Painel Administrativo:** Interface completa para gestão de pedidos, usuários e inventário.
* **Arquitetura Cloud:** Deploy automatizado em ambiente de nuvem.
* **Segurança:** Variáveis de ambiente protegidas e isolamento de processos via containers.

---

## Arquitetura e Deploy

O diferencial deste projeto é a sua estrutura de **DevOps**:

* **Docker Hub:** A imagem da aplicação está versionada e disponível para pull.
* **PostgreSQL:** Banco de dados robusto rodando em container isolado.
* **AWS EC2:** Hospedagem em servidor Ubuntu na nuvem.
* **Ngrok:** Túnel seguro com suporte a HTTPS para comunicação com webhooks de pagamento.
* **Persistência:** Uso de Docker Volumes para manter dados do banco e arquivos de mídia (fotos de produtos) seguros.

---

## Como Executar o Projeto

Você pode rodar este projeto de duas formas:

### 1. Via Docker Hub

Crie um arquivo `docker-compose.yml` e cole o conteúdo abaixo:

```yaml
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
