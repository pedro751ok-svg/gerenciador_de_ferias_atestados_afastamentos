import pytest
from utils.configurações_cpf_senhas import Gerenciador_cpf,Senha_hash
from service.logins import Cadastro_e_login
from service.solicitacoes import Solicitacao_service
from domain.constantes_de_status import StatusInss,StatEnum
from models.dados_dos_funcionarios import Funcionarios,TipoDeSolicitacao
from datetime import datetime
def test_cpf():
    assert Gerenciador_cpf.validar_cpf('52998224725') == True 
    assert Gerenciador_cpf.validar_cpf('12345678909') == True
def test_cpf_invalido():
    assert Gerenciador_cpf.validar_cpf('00000000000') == False
    assert Gerenciador_cpf.validar_cpf('12345678910') == False
def test_senha_hash():
    senha = 'progamtion54'
    assert Senha_hash.senha_hash(senha) is not None 
def test_chcar_senha():
    senha = 'progamation54'
    hash_gerado = Senha_hash.senha_hash(senha)

    assert Senha_hash.validar_senha(senha, hash_gerado) == True


def test_cadastrar(db_test):
    nome = "pedro"
    email = "pedro751@gamil.com"
    cpf = "55326653893"
    senha = "pedro751"
    role = "gerente"
    setor = "producao"
    ativo = True
    db = db_test
    novo_funcionario = Cadastro_e_login.cadastro_de_usuario(
        nome=nome,
        email=email,
        cpf = cpf,
        senha = senha,
        role = role,
        setor = setor,
        ativo= ativo,
        db = db

        )
    
    registro = db_test.query(Funcionarios).filter_by(email = "pedro751@gamil.com").first()
    assert registro is not None
    assert registro.nome == "pedro"
    assert registro.senha != "pedro751"
    print(type(novo_funcionario))
    print(novo_funcionario)
    
def test_login(db_test,funcionario_test):
    senha = "senha123"
    resultado = Cadastro_e_login.login_funcionario(
                                cpf = funcionario_test.cpf,
                                senha=senha,db = db_test)
    assert resultado is not None
    
    assert resultado.cpf == funcionario_test.cpf
    assert resultado.senha == funcionario_test.senha

def test_mandar_solicitacao(db_test):
        descricao = "atestado"
        ativo = True
        db = db_test

        resultado = Solicitacao_service.tipo_de_solicitacao(
            descricao=descricao,
            ativo=ativo,
            db = db
        )

        
        registro = db_test.query(TipoDeSolicitacao).filter_by(descricao = descricao).first()
        assert registro is not None
        assert registro.descricao == descricao
        assert resultado.ativo == ativo

def test_gerenciar_solicitacoes(db_test,funcionario_test,tipo_de_solicitacao_test):
     data_inicio = datetime(2026,7,7)
     data_fim = datetime(2026,7,8,)
     dados_extra = {"codigo_especie": StatusInss.B31}
     resultado = Solicitacao_service.gerenciador_solicitacoes(        
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_funcionario=funcionario_test.id,
        id_tipo=tipo_de_solicitacao_test.id,
        dados_extras=dados_extra,
        db=db_test)
     assert resultado is not None
     assert not isinstance(resultado,str)
     assert resultado.id_funcionario == funcionario_test.id
def test_aceitar_solicitacao(db_test,teste_de_solicitacoes,funcionario_test):
    resultado = Solicitacao_service.aceitar_solicitacao(id_solicitacao=teste_de_solicitacoes.id,aprovado_por=funcionario_test.id,db=db_test)
    assert resultado.status == StatEnum.aprovado

def test_rejeitar_solicitacoes(db_test,teste_de_solicitacoes,funcionario_test):
     resultado = Solicitacao_service.rejeitar_solicitacao(id_solicitacao=teste_de_solicitacoes.id,reprovado_por = funcionario_test.id,db = db_test)
     assert resultado.status == StatEnum.rejeitado
    
def test_cancelar_solicitacao(db_test,teste_de_solicitacoes):
     resultado = Solicitacao_service.cancelar_solicitacao(id_solicitacao=teste_de_solicitacoes.id,db = db_test)
     assert resultado.status == StatEnum.cancelado

def test_atualizar_solicitacao(db_test,teste_de_solicitacoes,funcionario_test,tipo_de_solicitacao_test):
    data_inicio = datetime(2027,8,1)
    data_fim = datetime(2027,9,2)
    resultado = Solicitacao_service.atualizar_solicitacao(
          id_solicitacao = teste_de_solicitacoes.id,
          id_tipo = tipo_de_solicitacao_test.id,
          data_inicio = data_inicio,
          data_fim = data_fim,
          db = db_test)
    assert resultado is not None
    assert resultado.data_inicio == data_inicio
    assert resultado.data_fim == data_fim