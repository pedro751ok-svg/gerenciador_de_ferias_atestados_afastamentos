import pytest
from database.banco_de_testes import session_teste,engine 
from models.dados_dos_funcionarios import TipoDeSolicitacao,Funcionarios,Solicitacoes,Base
from domain.constantes_de_status import Roleenum,DescricaoEnum,StatusInss
from datetime import datetime
from utils.configurações_cpf_senhas import Senha_hash
@pytest.fixture()
def db_test():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    conection = engine.connect()
    transacao = conection.begin()
    session = session_teste(bind =conection)
    yield session

    session.close()
    transacao.rollback()
    conection.close()

@pytest.fixture
def funcionario_test(db_test):
    senha = "senha123"
    senha_cp = Senha_hash.senha_hash(senha)
    funcionario_de_test = Funcionarios(
    nome="Teste",
    email="teste@teste.com",
    cpf="00000000000",
    senha= senha_cp,
    role=Roleenum.gerente,
    setor="producao",
    ativo=True
    )
    db_test.add(funcionario_de_test)
    db_test.flush()
    return funcionario_de_test
@pytest.fixture
def tipo_de_solicitacao_test(db_test):
    tipo_solicitacao_test = TipoDeSolicitacao(descricao = DescricaoEnum.afastamento)
    db_test.add(tipo_solicitacao_test)
    db_test.flush()
    return tipo_solicitacao_test
@pytest.fixture
def teste_de_solicitacoes(db_test,funcionario_test,tipo_de_solicitacao_test):
    data_inicio = datetime(2026,7,7)
    data_fim = datetime(2026,7,8,)
    resultado = Solicitacoes(        
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_funcionario=funcionario_test.id,
        id_tipo=tipo_de_solicitacao_test.id
    )
    db_test.add(resultado)
    db_test.flush()
    return resultado
