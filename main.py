from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configuração do Banco de Dados SQLite
DATABASE_URL = "sqlite:///./financas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do Banco de Dados
class TransacaoDB(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    valor = Column(Float)
    tipo = Column(String)  # 'receita' ou 'despesa'
    categoria = Column(String)

Base.metadata.create_all(bind=engine)

# Modelos de Validação (Pydantic)
class TransacaoCreate(BaseModel):
    descricao: str
    valor: float
    tipo: str
    categoria: str

class TransacaoResponse(TransacaoCreate):
    id: int

    class Config:
        from_attributes = True

# Inicialização do FastAPI
app = FastAPI(title="API de Controle de Finanças Pessoais")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas
@app.post("/transacoes/", response_model=TransacaoResponse, status_code=201)
def criar_transacao(transacao: TransacaoCreate, db: Session = Depends(get_db)):
    if transacao.tipo.lower() not in ["receita", "despesa"]:
        raise HTTPException(status_code=400, detail="O tipo deve ser 'receita' ou 'despesa'.")
    nova_transacao = TransacaoDB(**transacao.dict())
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return nova_transacao

@app.get("/transacoes/", response_model=List[TransacaoResponse])
def listar_transacoes(db: Session = Depends(get_db)):
    return db.query(TransacaoDB).all()

@app.get("/transacoes/resumo/")
def obter_resumo(db: Session = Depends(get_db)):
    transacoes = db.query(TransacaoDB).all()
    total_receitas = sum(t.valor for t in transacoes if t.tipo.lower() == "receita")
    total_despesas = sum(t.valor for t in transacoes if t.tipo.lower() == "despesa")
    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo_atual": total_receitas - total_despesas
    }