from domain.ferias_atestados_afastamentos import Afastamento_Inss
from domain.constantes_de_status import StatEnum
from models.dados_dos_funcionarios import Afastamentos_INSS


class AfastamentoValidador:

    @staticmethod
    def gerenciar_afastamento(id_solicitacao, tipo_de_solicitacao,codigo_especie, db):
        afastamento = (
            db.query(Afastamentos_INSS)
            .filter_by(id_solicitacao=id_solicitacao)
            .first()
        )
        if not afastamento:
            raise ValueError("Nenhum afastamento encontrado")

        resultado = Afastamentos_INSS.afastado_pelo_inss(
            id_solicitacao=id_solicitacao,
            tipo_de_solicitacao=tipo_de_solicitacao,
        )
        if resultado != StatEnum.pendente:
            raise ValueError(f"Regra de afastamento violada: {resultado}")

        afastamento.codigo_especie = codigo_especie
        db.flush()
        return afastamento