from sqlalchemy import create_engine,Column,String,Integer,DateTime,Enum,Boolean,ForeignKey
import enum
from datetime import datetime
from domain.constantes_de_status import DescricaoEnum,StatEnum,Roleenum,StatusInss
from sqlalchemy.orm import declarative_base,sessionmaker,relationship
engine = create_engine("postgresql://postgres:bolhas@localhost:5432/sistema_ferias")
Base = declarative_base()
session = sessionmaker(bind=engine)

class Funcionarios(Base):
    __tablename__ = "funcionarios"
    id = Column(Integer,primary_key=True)
    nome = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    cpf = Column(String,unique=True)
    senha = Column(String,nullable=False) 

    role = Column(Enum(Roleenum),nullable=False)
    setor = Column(String,nullable=False)
    ativo = Column(Boolean,default=True)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    
class TipoDeSolicitacao(Base):
    __tablename__ = "tipo"
    id_funcionario = Column(Integer,primary_key=True)
    descricao = Column(Enum(DescricaoEnum),nullable=False)
    ativo = Column(Boolean,default=True)

class Solicitacoes(Base):
    __tablename__ = "solicitacoes"

    id = Column(Integer, primary_key=True)
    id_funcionario = Column(Integer, ForeignKey("funcionarios.id"))
    id_tipo = Column(Integer, ForeignKey("tipo.id"))

    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)

    status = Column(Enum(StatEnum), nullable=False, default=StatEnum.pendente)

    aprovado_por = Column(Integer, ForeignKey("funcionarios.id"))
    reprovado_por = Column(Integer, ForeignKey("funcionarios.id"))

    criado_em = Column(DateTime, default=datetime.utcnow)
    aprovado_em = Column(DateTime, nullable=True)
    reprovado_em = Column(DateTime, nullable=True)

    ferias = relationship("Ferias", back_populates="solicitacao")
    atestados = relationship("Atestados_funcionarios", back_populates="solicitacao")
    afastamentos = relationship("Afastamentos_INSS", back_populates="solicitacao")


class Atestados_funcionarios(Base):
    __tablename__ = "atestados"

    id = Column(Integer, primary_key=True)
    id_solicitacao = Column(Integer, ForeignKey("solicitacoes.id"))
    cid = Column(String)

    solicitacao = relationship("Solicitacoes", back_populates="atestados")


class Afastamentos_INSS(Base):
    __tablename__ = "afastamentos"

    id = Column(Integer, primary_key=True)
    id_solicitacao = Column(Integer, ForeignKey("solicitacoes.id"))
    codigo_especie = Column(Enum(StatusInss), nullable=False)

    solicitacao = relationship("Solicitacoes", back_populates="afastamentos")


class Ferias(Base):
    __tablename__ = "ferias"

    id = Column(Integer, primary_key=True)
    id_solicitacao = Column(Integer, ForeignKey("solicitacoes.id"))

    solicitacao = relationship("Solicitacoes", back_populates="ferias")