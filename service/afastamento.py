from domain.ferias_atestados_afastamentos import AfastamentoInss
from domain.constantes_de_status import StatEnum
from models.dados_dos_funcionarios import Afastamentos_INSS


class AfastamentoValidador:

    @staticmethod
    def gerenciar_afastamento(id_solicitacao, data_inicio,data_fim,codigo_especie, db):
        afastamento = (
            db.query(Afastamentos_INSS)
            .filter_by(id_solicitacao=id_solicitacao)
            .first()
        )
        if not afastamento:
            raise ValueError("Nenhum afastamento encontrado")

        resultado = AfastamentoInss.afastado_pelo_inss(
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        if resultado != StatEnum.pendente:
            raise ValueError(f"Regra de afastamento violada: {resultado}")

        afastamento.codigo_especie = codigo_especie
        db.flush()
        return afastamento