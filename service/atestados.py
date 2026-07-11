from domain.ferias_atestados_afastamentos import Atestado
from models.dados_dos_funcionarios import Solicitacoes, Atestados_funcionarios


class AtestadoValidador:
    @staticmethod
    def regras_de_atestados(id_solicitacao, db):
        solicitacao = db.query(Solicitacoes).filter_by(id=id_solicitacao).first()
        if not solicitacao:
            raise ValueError("Nenhuma solicitação encontrada")

        if solicitacao.data_fim < solicitacao.data_inicio:
            raise ValueError("Datas da solicitação são inválidas")

        solicitacao.status = Atestado.regras_atestado_medico(
            data_inicio=solicitacao.data_inicio,
            data_fim=solicitacao.data_fim,
        )
        db.flush()
        return solicitacao

    @staticmethod
    def definir_cid(cid: str, id_solicitacao, db):
        atestado = db.query(Atestados_funcionarios).filter_by(id_solicitacao=id_solicitacao).first()
        if not atestado:
            raise ValueError("Atestado não encontrado")

        atestado.cid = cid
        db.flush()
        return atestado