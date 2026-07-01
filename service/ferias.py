from models.dados_dos_funcionarios import Solicitacoes,session
from domain.ferias_atestados_afastamentos import Regras_ferias
from domain.constantes_de_status import StatEnum
class Ferias:
    
    @staticmethod
    def ferias(id_ferias,data_fim,data_inicio):
        resultado = Regras_ferias.regras_ferias(
            data_inicio=data_inicio,
            data_fim=data_fim
            )
        if resultado != StatEnum.pendente:
            return resultado
    
        with session() as sessao:
            ferias_existentes = (sessao.query(Solicitacoes).filter(
                Solicitacoes.id_funcionario == id_ferias,
                Solicitacoes.status == StatEnum.aprovado,
                Solicitacoes.data_inicio <= data_fim,
                Solicitacoes.data_fim >= data_inicio
                ).first())
            
            if ferias_existentes:
                if Regras_ferias.vericar_expiracao(ferias_existentes.data_inicio):
                    ferias_existentes.status = StatEnum.expirado
                    sessao.commit()
                return "esse funcionario ja esta com uma ferias ativa"
            sessao.commit()
            return "nenhuma ferias encontrada no momento"
            