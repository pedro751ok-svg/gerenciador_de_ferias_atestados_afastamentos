from domain.controleDeAcesso import ControleAcesso
from models.dados_dos_funcionarios import Funcionarios,session
class SolicitacoesServices:
    @staticmethod
    def criar(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()
            
            if not ControleAcesso.controle_de_acesso(funcionario.role,"criar_solicitacao"):
                return "sem permissao"
            return "solicitacao criada com sucesso"
    @staticmethod    
    def cancelar(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()

            if not ControleAcesso.controle_de_acesso(funcionario.role,"cancelar_solicitacao"):
                return "sem permissao"
            return "cancelamento feito com sucesso"
    @staticmethod
    def aceitar(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()

            if not ControleAcesso.controle_de_acesso(funcionario.role,"aceitar_solicitacao"):
                return "sem permissao"
            return "solicitação aceita"
    @staticmethod
    def rejeitar(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()

            if not ControleAcesso.controle_de_acesso(funcionario.role,"rejeitar_solicitacao"):
                return "sem permissao"
            return "solicitação reijeitada"
    @staticmethod
    def exibir_solicitacoes(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()

            if not ControleAcesso.controle_de_acesso(funcionario.role,"exibir_solicitacao"):
                return "sem permissao"
            return "permissao aceita"
    @staticmethod
    def gerenciar_cid(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()

            if not ControleAcesso.controle_de_acesso(funcionario.role,"gerenciar_cid"):
                return "sem permissao"
            return "permissao aceita"
    @staticmethod
    def gerenciar_afastamento(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()

            if not ControleAcesso.controle_de_acesso(funcionario.role,"gerenciar_afastamento"):
                return "sem permissao"
            return "permissao aceita"
    @staticmethod
    def historico_solicitacoes(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()

            if not ControleAcesso.controle_de_acesso(funcionario.role,"historico_solicitacoes"):
                return "sem permissao"
            return "permissao aceita"
    @staticmethod
    def listar_solicitacoes_pendentes(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()

            if not ControleAcesso.controle_de_acesso(funcionario.role,"listar_solicitacoes_pendentes"):
                return "sem permissao"
            return "permissao aceita"
    @staticmethod
    def gerenciar_solicitacoes(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()

            if not ControleAcesso.controle_de_acesso(funcionario.role,"gerenciar_solicitacoes"):
                return "sem permissao"
            return "permissao aceita"
    @staticmethod
    def cancelar_solicitacao(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()
            if not ControleAcesso.controle_de_acesso(funcionario.role,"cancelar_solicitacao"):
                return "sem prmição paraz fazer cancelamentos"
            return "permissao aceita"
    @staticmethod
    def atualizar_solicitacao(id_funcionario):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()
            if not ControleAcesso.controle_de_acesso(funcionario.role ,"atualizar_solicitacao"):
                return "sem permissao para atualizar solicitacoes"
            return "permissao aceita"
    @staticmethod
    def cadastrar_funcionario(id_funcionario):
        with session() as sessao:   
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()
            if not ControleAcesso.controle_de_acesso(funcionario.role,"cadastrar_funcionario"):
                return "sem permissao para essa ação"
            return "permissao aceita"