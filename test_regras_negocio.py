import pytest
from utils.configurações_cpf_senhas import Gerenciador_cpf,Senha_hash
from service.logins import Cadastro_e_login
from service.solicitacoes import Solicitacao_service
from domain.constantes_de_status import DescricaoEnum
from models.dados_dos_funcionarios import Funcionarios,TipoDeSolicitacao
from database.banco_de_testes import session_teste]
import datetime
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
#teste de llogin 
@pytest.fixture
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
@pytest.fixture
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
@pytest.fixture
def gerenciar(db_test):
     data_inicio = datetime(07/07/2026)
     data_fim = datetime(07/08/2026)
     dados_extra = {"codoigo especie: B31"}
     resultado = Solicitacao_service.gerenciador_solicitacoes(        
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_funcionario=test_cadastrar.id,
        id_tipo=test_mandar_solicitacao.id,
        dados_extras=dados_extra,
        db=db_test)
     assert resultado is not None
     assert not isinstance(resultado,str)
     assert resultado.id_funcionario == test_cadastrar.id

     #data_inicio:int,data_fim:int,id_funcionario:int,id_tipo:int,dados_extras:str,db = None