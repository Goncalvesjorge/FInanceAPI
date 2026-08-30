# 💰 API de Controle de Finanças Pessoais (FinanceAPI)

API REST desenvolvida em Python para gerenciamento de finanças pessoais, permitindo registrar receitas, despesas, consultar transações e acompanhar o saldo atual em tempo real.

## 🚀 Tecnologias Utilizadas
* **Python 3.10+**
* **FastAPI**: Framework web de alta performance.
* **SQLite**: Banco de dados relacional leve para armazenamento local.
* **SQLAlchemy**: ORM para manipulação simplificada do banco de dados.
* **Uvicorn**: Servidor ASGI de rápida execução.

## 📌 Funcionalidades da API
- `POST /transacoes/`: Cadastra uma nova receita ou despesa.
- `GET /transacoes/`: Lista todas as movimentações financeiras salvas.
- `GET /transacoes/resumo/`: Exibe o cálculo automático de total de receitas, despesas e saldo final.
- `DELETE /transacoes/{id}`: Remove uma movimentação pelo ID.

## 🛠️ Como executar o projeto localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Goncalvesjorge/FinanceAPI.git](https://github.com/Goncalvesjorge/FinanceAPI.git)
   cd FinanceAPI
