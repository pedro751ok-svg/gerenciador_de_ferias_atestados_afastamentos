from domain.ferias_atestados_afastamentos import Regrasferias
from domain.constantes_de_status import StatEnum
from models.dados_dos_funcionarios import Solicitacoes


class FeriasValidador:

    @staticmethod
    def validar(id_funcionario, data_inicio, data_fim, db):
        resultado = Regrasferias.regras_ferias(
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        if resultado != StatEnum.pendente:
            raise ValueError(f"Regra de férias violada: {resultado}")

        ferias_existentes = (
            db.query(Solicitacoes)
            .filter(
                Solicitacoes.id_funcionario == id_funcionario,
                Solicitacoes.status == StatEnum.aprovado,
                Solicitacoes.data_inicio <= data_fim,
                Solicitacoes.data_fim >= data_inicio,
            )
            .first()
        )

        if ferias_existentes:
            if Regrasferias.vericar_expiracao(ferias_existentes.data_inicio):
                ferias_existentes.status = StatEnum.expirado
                db.flush()
            else:
                raise ValueError("Esse funcionário já está com férias ativas")