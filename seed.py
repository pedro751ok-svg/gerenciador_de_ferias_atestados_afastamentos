from models.dados_dos_funcionarios import Base, engine, session, Funcionarios
from domain.constantes_de_status import Roleenum
from utils.configurações_cpf_senhas import Senha_hash
from dotenv import load_dotenv
import os 
load_dotenv()
Base.metadata.create_all(engine)

with session() as db:
    existe = db.query(Funcionarios).filter_by(cpf=os.getenv("SEED_CPF")).first()
    if not existe:
        admin = Funcionarios(
            nome="Admin RH",
            email="admin@empresa.com",
            cpf=os.getenv("SEED_CPF"),
            senha=Senha_hash.senha_hash(os.getenv("SEED_SENHA")),
            role=Roleenum.rh,
            setor="rh",
            ativo=True
        )
        db.add(admin)
        db.commit()
        print("Usuário RH inicial criado.")
    else:
        print("Já existe um usuário com esse CPF, nada foi feito.")