from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.dados_dos_funcionarios import Base
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.dados_dos_funcionarios import Base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "teste.db")

engine = create_engine(
    f"sqlite:///memory",
    connect_args={"check_same_thread": False}
)
session_teste = sessionmaker(bind=engine)

