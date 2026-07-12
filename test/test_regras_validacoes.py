import pytest
from service.logins import Cadastro_e_login
from service.solicitacoes import Solicitacao_service
from domain.constantes_de_status import StatEnum
from models.dados_dos_funcionarios import Funcionarios
from datetime import datetime
def test_funcionario_ja_existe(db_test,funcionario_test):
    novo_funcionario = Cadastro_e_login.cadastro_de_usuario(
        nome=funcionario_test.nome,
        email=funcionario_test.email,
        cpf = funcionario_test.cpf,
        senha = funcionario_test.senha,
        role = funcionario_test.role,
        setor = funcionario_test.setor,
        ativo= funcionario_test.ativo,
        db = db_test

        )
    
    registro = db_test.query(Funcionarios).filter_by(email = "pedro751@gamil.com").first()
    assert registro is None
    print(type(novo_funcionario))
    print(novo_funcionario)

def test_validacao_login_dados_false(db_test):
    senha = "senha"
    cpf = "002992929299"
    email = "pedro@gmail.com"
    resultado = Cadastro_e_login.login_funcionario(
                                cpf = cpf,
                                senha=senha,db = db_test)

    assert isinstance(resultado,str)
    assert resultado == "funcionario nao existe"
def test_validacao_login_senha_errada(db_test,funcionario_test):
    senha = "senha"
    resultado = Cadastro_e_login.login_funcionario(
                                cpf = funcionario_test.cpf,
                                senha=senha,db = db_test)
    assert resultado == "senha invalida tente novamente"

def test_gerenciador_funcionario_nao_encontrado(db_test, tipo_de_solicitacao_test):
    
    data_inicio = datetime(2026, 7, 7)
    data_fim = datetime(2026, 7, 8)
    with pytest.raises(ValueError) as exc_info:
        Solicitacao_service.gerenciador_solicitacoes(
            data_inicio=data_inicio,
            data_fim=data_fim,
            id_funcionario=9999,  
            id_tipo=tipo_de_solicitacao_test.id,
            dados_extras="{}",
            db=db_test
        )
    
    assert "funcionario nao encontrado" in str(exc_info.value)


def test_gerenciador_datas_nao_coincidem(db_test, funcionario_test, tipo_de_solicitacao_test):
   
    data_inicio = datetime(2026, 7, 8)
    data_fim = datetime(2026, 7, 7) 
    with pytest.raises(ValueError) as exc_info:
        Solicitacao_service.gerenciador_solicitacoes(
            data_inicio=data_inicio,
            data_fim=data_fim,
            id_funcionario=funcionario_test.id,
            id_tipo=tipo_de_solicitacao_test.id,
            dados_extras="{}",
            db=db_test
        )
    
    assert " as datas nao concidem" in str(exc_info.value)

def test_gerenciador_solicitacao_pendente_existente(db_test, funcionario_test, tipo_de_solicitacao_test, teste_de_solicitacoes):
    teste_de_solicitacoes.status = StatEnum.pendente
    db_test.flush()
    
    data_inicio = datetime(2026, 7, 10)
    data_fim = datetime(2026, 7, 12)
    with pytest.raises(ValueError) as exc_info:
        Solicitacao_service.gerenciador_solicitacoes(
            data_inicio=data_inicio,
            data_fim=data_fim,
            id_funcionario=funcionario_test.id,
            id_tipo=tipo_de_solicitacao_test.id,
            dados_extras="{}",
            db=db_test
        )
    
    assert "funcionario ja esta com uma solicitacao pendente" in str(exc_info.value)

def test_aceitar_solicitacao_nao_encontrada(db_test):
   
    with pytest.raises(ValueError) as exc_info:
        Solicitacao_service.aceitar_solicitacao(
            id_solicitacao=9999,  
            aprovado_por=1,
            db=db_test
        )
    
    assert "nenhuma solicitacao encontrada com esse id" in str(exc_info.value)


def test_aceitar_solicitacao_nao_pendente(db_test, teste_de_solicitacoes):

    teste_de_solicitacoes.status = StatEnum.aprovado
    db_test.flush()

    with pytest.raises(ValueError) as exc_info:
        Solicitacao_service.aceitar_solicitacao(
            id_solicitacao=teste_de_solicitacoes.id,
            aprovado_por=1,
            db=db_test
        )
    
    assert "solicitacao nao esta pendente" in str(exc_info.value)

def test_rejeitar_solicitacao_nao_encontrada(db_test):

    resultado = Solicitacao_service.rejeitar_solicitacao(
        id_solicitacao=9999,
        reprovado_por=1,
        db=db_test
    )
    
    assert resultado == "falha na sessao"


def test_rejeitar_solicitacao_nao_pendente(db_test, teste_de_solicitacoes):
   
    teste_de_solicitacoes.status = StatEnum.rejeitado
    db_test.flush()

    
    resultado = Solicitacao_service.rejeitar_solicitacao(
        id_solicitacao=teste_de_solicitacoes.id,
        reprovado_por=1,
        db=db_test
    )
    
    assert resultado == "falha na sessao"