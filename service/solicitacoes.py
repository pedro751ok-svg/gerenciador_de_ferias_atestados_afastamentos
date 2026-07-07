from models.dados_dos_funcionarios import Funcionarios,Solicitacoes,session,TipoDeSolicitacao,Ferias,Afastamentos_INSS,Atestados_funcionarios
from domain.constantes_de_status import StatEnum,DescricaoEnum
from domain.controleDeAcesso import ControleAcesso
from domain.regras_de_status import Regrasdestatus
from datetime import datetime
from service.ferias import FeriasValidador


class Solicitacao_service:

    @staticmethod
    def tipo_de_solicitacao(descricao:str,ativo:bool,db =None):
        if db is None:
            db = session()
            close_db = True
        else:
            close_db = False
        try:    
            mandar_solicitacao = TipoDeSolicitacao(
                descricao = descricao,
                ativo = ativo
                )
            db.add(mandar_solicitacao)
            db.commit()
            return mandar_solicitacao
        except:
            db.rollback()
        finally:
            if close_db:
                db.close()

    @staticmethod
    def gerenciador_solicitacoes(data_inicio:datetime,data_fim:datetime,id_funcionario:int,id_tipo:int,dados_extras:str,db = None):
        if db is None:
            db = session()
            close_db = True
        else:
            close_db = False
        try:
            funcionario = db.query(Funcionarios).filter_by(id = id_funcionario).first()
            if not funcionario:
                return "funcionario nao encontrado "
            
            if data_fim < data_inicio:
                return " as datas nao concidem"
            
            tipo = db.query(TipoDeSolicitacao).filter_by(id=id_tipo).first()
            if not tipo:
                return "tipo de solicitção não encontrada"
            
            controle_solicitacoes = db.query(Solicitacoes).filter(
                Solicitacoes.id_funcionario == id_funcionario,
                Solicitacoes.status == StatEnum.pendente).first()
            if controle_solicitacoes:
                return "funcionario ja esta com uma solicitacao pendente"
            
            if tipo.descricao == DescricaoEnum.ferias:
                FeriasValidador.validar(id_funcionario, data_inicio, data_fim, db)
            
            solicitacao = Solicitacoes(
                id_tipo = id_tipo,
                id_funcionario = id_funcionario,
                data_inicio = data_inicio,
                data_fim = data_fim
            )

            db.add(solicitacao)
            db.flush()
            Solicitacao_service._criar_registro_filho(
                tipo.descricao,solicitacao.id,dados_extras,db
            )
            db.commit()
            return solicitacao
        except Exception:
            db.rollback()
            raise
        finally:
            if close_db:
                db.close()

    @staticmethod
    def _criar_registro_filho(descricao_tipo, id_solicitacao, dados_extra, db):
        dados_extra = dados_extra or {}
        if descricao_tipo == DescricaoEnum.ferias:
            db.add(Ferias(id_solicitacao=id_solicitacao))

        elif descricao_tipo == DescricaoEnum.atestado:
            db.add(Atestados_funcionarios(id_solicitacao=id_solicitacao,cid=dados_extra.get("cid")))

        elif descricao_tipo == DescricaoEnum.afastamento:
            db.add(Afastamentos_INSS(id_solicitacao=id_solicitacao,codigo_especie=dados_extra.get("codigo_especie")))
        else:
            raise ValueError("tipo de solicitacao desconhecido")

    @staticmethod
    def exibir_solicitacao(id_solicitacao:int,db: None):
        if db is None:
            db = session()
            close_db = True
        else:
            close_db = False
        try:
            ver_solicitacoes = db.query(Solicitacoes).filter_by(id = id_solicitacao).first()
            if not ver_solicitacoes:
                raise ValueError("nenhuma solicitacao encontrada ")
            
            return ver_solicitacoes
        except Exception as e:
            raise ValueError(f"erro em {e}")
        finally:
            if close_db:
                db.close()
        
    @staticmethod
    def aceitar_solicitacao(id_solicitacao,aprovado_por, db = None):
        if db is None:
            db = session()
            close_db = True
        else:
            close_db = False
        try:
            solicitacao = db.query(Solicitacoes).filter_by(id = id_solicitacao).first()
            if not solicitacao:
                raise ValueError ("nenhuma solicitacao encontrada com esse id ")
            if solicitacao.status != StatEnum.pendente:
                raise ValueError("solicitacao nao esta pendente")
            Regrasdestatus.status_regras(solicitacao)
            solicitacao.status = StatEnum.aprovado
            solicitacao.aprovado_por = aprovado_por

            db.commit()
            return solicitacao
        except:
                db.rollback()
                return "falha na sessao"
        finally:
            if close_db:
                db.close()
    @staticmethod
    def rejeitar_solicitacao(id_solicitacao,reprovado_por, db = None):
        if db is None:
            db = session()
            close_db = True
        else:
            close_db - False
        try:
            solicitacao = db.query(Solicitacoes).filter_by(id = id_solicitacao).first()
            if not solicitacao:
                raise ValueError ("nenhuma solicitacao pendente")
            if solicitacao.status != StatEnum.pendente:
                raise ValueError("solicitacao nao esta pendente")
            Regrasdestatus.status_regras(solicitacao)
            solicitacao.status = StatEnum.rejeitado
            solicitacao.reprovado_por = reprovado_por
            db.commit()
            return solicitacao
        except:
            db.rollback()
            return "falha na sessao"
        finally:
            if close_db:
                db.close()

    @staticmethod
    def historico_solicitacoes(id_solicitacao):
        with session() as sessao:
            ver_solicitacoes = sessao.query(Solicitacoes).filter_by(id = id_solicitacao).all()
            if not ver_solicitacoes:
                return " nenhum solicitacao ate o momento"
            return ver_solicitacoes 

    @staticmethod
    def cancelar_solicitacao(id_solicitacao, db = None):
        if db is None:
            db = session()
            close_db = True
        else:
            close_db = False
        try:
            cancel_solicitacao = db.query(Solicitacoes).filter_by(id = id_solicitacao).first()
            if not cancel_solicitacao:
                raise ValueError("nenhuma solicitacao encontradar")
            if cancel_solicitacao.status == StatEnum.aprovado:
                raise ValueError("impossivel cancelar solicitacao no momento")
            cancel_solicitacao.status = StatEnum.cancelado
                
            db.commit()
            return "solicitacao cancelada com sucesso"
        except:
            db.rollback()
            return "falha na sessao"
        finally:
            if close_db:
                db.close()

    @staticmethod
    def listar_solicitações_pendentes(solicitacao_status):
        with session() as sessao:
            solicitacoes = sessao.query(Solicitacoes).filter_by(status = solicitacao_status).all()
            if not solicitacoes:
                return "nenhuma solicitação pendente"
            return solicitacoes

    @staticmethod
    def atualizar_solicitacao(id_solicitacao:int,id_tipo:int = None,data_inicio:datetime = None,data_fim:datetime = None):
        try:
            with session() as sessao:
                solicitacao = sessao.query(Solicitacoes).filter_by(id = id_solicitacao).first()
            
                if not solicitacao:
                    raise ValueError ("nenhum funcionario encontrado")
                if solicitacao.status != StatEnum.pendente:
                    raise ValueError ("so e possivel alterar solicitacoes pendentes")
                if id_tipo:
                    solicitacao.id_tipo = id_tipo
                if data_inicio:
                    solicitacao.data_inicio = data_inicio
                if data_fim:
                    solicitacao.data_fim = data_fim
                sessao.commit()
                sessao.refresh(solicitacao)
                return solicitacao
        except Exception as e:
            sessao.rollback()
            raise