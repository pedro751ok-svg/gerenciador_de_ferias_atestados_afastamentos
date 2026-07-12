from flask import Blueprint
from controller.controllers import ControleGeral
from middleware.rbac import requer_permissao
from middleware.token_de_acesso import requer_token
rota = Blueprint("rota",__name__)
@rota.route("/cadastro",methods = ["POST"])
@requer_permissao("cadastrar_funcionario")
def cadastrar():
    return ControleGeral.controlle_de_cadastros()

@rota.route("/login",methods = ["POST"])
@requer_token
def login():
    return ControleGeral.controlle_de_logins()

@rota.route("/tipo-solicitacao",methods = ["POST"])
@requer_token
@requer_permissao("criar_solicitacao")
def tipo_solicitacao():
    return ControleGeral.controlle_tipo_de_solicitacao()

@rota.route("/gerenciador-solicitacoes",methods = ["POST"])
@requer_token
@requer_permissao("gerenciar_solicitacoes")
def gerenciar_solicitacoes():
    return ControleGeral.controlle_gerenciador_de_solicitacoes()

@rota.route("/aceitar-solicitacao",methods = ["POST"])
@requer_token
@requer_permissao("aceitar_solicitacao")
def aceitar_solicitacao():
    return ControleGeral.controlle_aceitar_solicitacoes()

@rota.route("/rejeitar-solicitacao",methods = ["POST"])
@requer_token
@requer_permissao("rejeitar_solicitacao")
def rejeitar_solicitacao():
    return ControleGeral.controlle_rejeitar_solicitacao()

@rota.route("/cancelar-solicitacao",methods = ["POST"])
@requer_token
@requer_permissao("cancelar_solicitacao")
def cancelar_solicitacao():
    return ControleGeral.controlle_cancelar_solicitacoes()

@rota.route("/atualizar-solicitacao",methods = ["POST"])
@requer_token
@requer_permissao("atualizar_solicitacao")
def atualizar_solicitacao():
    return ControleGeral.controlle_atualizar_solicitacoes()

@rota.route("/gerenciar-cid",methods = ["PUT"])
@requer_token
@requer_permissao("gerenciar_cid")
def gernciar_cids():
    return ControleGeral.controlle_atestados()

@rota.route("/gerenciar-afastamentos-codigo_especie",methods = ["PUT"])
@requer_token
@requer_permissao("gerenciar_afastamento")
def gerenciar_afastamentos():
    return ControleGeral.controlle_afastamentos()

@rota.route("/exibir-solicitacao",methods = ["GET"])
@requer_token
@requer_permissao("exibir_soolicitacao")
def exibir():
    return ControleGeral.controlle_exibir_solicitacao()

@rota.route("/exibir-historico-solicitacoes",methods = ["GET"])
@requer_token
@requer_permissao("historico_solicitacoes")
def gerenciar_historico_solicitacoes():
    return ControleGeral.controlle_historico_de_solicitacoes()

@rota.route("/exibir-solicitacoes-pendentes",methods = ["GET"])
@requer_token
@requer_permissao("listar_solicitacoes_pendentes")
def listar_solicitacoes_pendentes():
    return ControleGeral.controlle_solicitacoes_pendentes()
