import pytest
from utils.configurações_cpf_senhas import Gerenciador_cpf,Senha_hash
from service.logins import Cadastro_e_login
from service.solicitacoes import solicitacao_service
from domain.constantes_de_status import DescricaoEnum
from models.dados_dos_funcionarios import Funcionarios
from database.banco_de_testes import session_teste
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
def test_cadastrar():
    with session_teste() as sessao:
        nome = "pedro"
        email = "pedro751@gamil.com"
        cpf = "55326653893"
        senha = "pedro751"
        role = "gerente"
        setor = "producao"
        ativo = True
        db = sessao
        novo_funcionario = Cadastro_e_login.cadastro_de_usuario(
            nome=nome,
            email=email,
            cpf = cpf,
            senha = senha,
            role = role,
            setor = setor,
            ativo= ativo
            db = sessao

        )
    assert novo_funcionario == "cadastrado com sucesso"
    print(type(novo_funcionario))
    print(novo_funcionario)
def test_mandar_solicitacao():
    with session_teste as sessao:
        descricao = "atestado"
        ativo = True

        resultado = solicitacao_service.tipo_de_solicitacao(
            descricao=descricao,
            ativo=ativo
        )

        assert resultado == "solicitação realizada"
        assert resultado.descricao == descricao
        assert resultado.ativo == ativo
def test_false_mandar_solicitacao():
    descricao = DescricaoEnum.atestado
    ativo = True
    resultado = solicitacao_service.tipo_de_solicitacao(
        descricao=descricao,
        ativo=ativo
    )
    assert resultado is not None
    assert resultado.descricao == descricao
    assert resultado.ativo == ativo