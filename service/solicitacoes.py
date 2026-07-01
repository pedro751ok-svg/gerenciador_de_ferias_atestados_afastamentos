from models.dados_dos_funcionarios import Funcionarios,Solicitacoes,session,TipoDeSolicitacao
from domain.constantes_de_status import StatEnum
from domain.controleDeAcesso import ControleAcesso
from domain.regras_de_status import Regrasdestatus
class solicitacao_service:

    @staticmethod
    def tipo_de_solicitacao(id_tipo_solicitacao:int,descricao:str,ativo:bool,db =None):
        if db is None:
            db = session()
            close_db = True
        else:
            close_db = False
        try:
            existe = db.query(TipoDeSolicitacao).filter_by(id_funcionario = id_tipo_solicitacao).first()
            if existe:
                return "funcionario ja tem uma solictação ativa"
            
            mandar_solicitacao = TipoDeSolicitacao(
                descricao = descricao,
                ativo = ativo
                )
            db.add(mandar_solicitacao)
            db.commit()
            return mandar_solicitacao
        finally:
            if close_db:
                db.close()
    @staticmethod
    def gerenciador_solicitacoes(data_inicio:int,data_fim:int,id_funcionario:int,id_tipo:int):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id = id_funcionario).first()
            if not funcionario:
                return "funcionario nao encontrado "
            if data_fim < data_inicio:
                return " as datas nao concidem"
            
            solicitacao = Solicitacoes(
                id_tipo = id_tipo,
                id_funcionario = id_funcionario,
                data_inicio = data_inicio,
                data_fim = data_fim
            )
            if data_fim < data_inicio:
                return " as datas nao concidem"
            
            sessao.add(solicitacao)
            sessao.commit()

    @staticmethod
    def exibir_solicitacao(id_tipo_solicitacao:int):
        with session() as sessao:
            ver_solicitacoes = sessao.query(TipoDeSolicitacao).filter_by(id = id_tipo_solicitacao).first()
            if not ver_solicitacoes:
                return "nenhuma solicitacao encontrada "
            
            return ver_solicitacoes
        
    @staticmethod
    def aceitar_solicitacao(id_solicitacao,aprovado_por):
        try:
            with session() as sessao:
                solicitacao = sessao.query(Solicitacoes).filter_by(id = id_solicitacao).first()
                if not solicitacao:
                    return "nenhuma solicitacao encontrada com esse id "
                if solicitacao.status != StatEnum.pendente:
                    return "solicitacao nao esta pendente"
                Regrasdestatus.status_regras(solicitacao)
                solicitacao.status = StatEnum.aprovado
                solicitacao.aprovado_por = aprovado_por

                sessao.commit()
                return solicitacao
        except:
            sessao.rollback()
            return "falha na sessao"
    @staticmethod
    def rejeitar_solicitacao(id_solicitacao,reprovado_por):
        try:
            with session() as sessao:
                solicitacao = sessao.query(Solicitacoes).filter_by(id = id_solicitacao).first()
                if not solicitacao:
                    return "nenhuma solicitacao pendente"
                if solicitacao.status != StatEnum.pendente:
                    return "solicitacao nao esta pendente"
                Regrasdestatus.status_regras(solicitacao)
                solicitacao.status = StatEnum.rejeitado
                solicitacao.reprovado_por = reprovado_por
                sessao.commit()
                return solicitacao
        except:
            sessao.rollback()
            return "falha na sessao"
    @staticmethod
    def historico_solicitacoes(id_solicitacao):
        with session() as sessao:
            ver_solicitacoes = sessao.query(Solicitacoes).filter_by(id = id_solicitacao).first()
            if not ver_solicitacoes:
                return " nenhum solicitacao ate o momento"
            return ver_solicitacoes 
    @staticmethod
    def cancelar_solicitacao(id_solicitacao):
        try:
            with session() as sessao:
                cancel_solicitacao = sessao.query(Solicitacoes).filter_by(id = id_solicitacao).first()
                if not cancel_solicitacao:
                    return "nenhuma solicitacao encontradar"
                if cancel_solicitacao.status == StatEnum.aprovado:
                    return "impossivel cancelar solicitacao no momento"
                cancel_solicitacao.status = StatEnum.cancelado
                
                sessao.commit()
                return "solicitacao cancelada com sucesso"
        except:
            sessao.rollback()
            return "falha na sessao"
    @staticmethod
    def listar_solicitações_pendentes(solicitacao_status):
        with session() as sessao:
            solicitacoes = sessao.query(Solicitacoes).filter_by(status = solicitacao_status).all()
            if not solicitacoes:
                return "nenhuma solicitação pendente"
            return solicitacoes