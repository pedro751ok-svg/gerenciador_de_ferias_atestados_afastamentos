from models.dados_dos_funcionarios import Afastamentos_INSS,session
from domain.ferias_atestados_afastamentos import Afastamento_Inss
from domain.constantes_de_status import StatEnum
class Afastamento:

    @staticmethod
    def gerenciar_afastamentos(id_afastamento, tipo_de_solicitacao):
        resultado = Afastamento_Inss.afastado_pelo_inss()
        if resultado != StatEnum.pendente:
            return resultado
        with session() as sessao:
            afastamento = (
                sessao.query(Afastamentos_INSS)
                .filter_by(id=id_afastamento)
                .first()
            )
            if not afastamento:
                return "nenhum afastamento encontrado nesse id"
            afastamento.codigo_especie = tipo_de_solicitacao
            sessao.commit()
            return afastamento