from domain.constantes_de_status import Statsnumber
from datetime import datetime
class Atestado:
    @staticmethod
    def regras_atestado_medico(data_inicio:datetime, data_fim:datetime):
        days_ = (data_fim - data_inicio).days + 1
        if days_ > 15:
            return Statsnumber.encaminhado_afastamento
        
        return Statsnumber.pendente
class AfastamentoInss:
    @staticmethod
    def afastado_pelo_inss(data_inicio:datetime, data_fim:datetime):
        days_ = (data_fim - data_inicio).days + 1
        if days_ <=0:
            raise ValueError("a data final deve ser maior que a data incio")
        return days_, Statsnumber.pendente
class Regrasferias:
    @staticmethod
    def regas_ferias(data_inicio:datetime,data_fim:datetime):
            dias = (data_fim - data_inicio).days + 1
            if dias <= 0 :
                raise ValueError("a data deve ser maior que a data de inicio")
            if dias > 30:
                raise ValueError("quantidade de dias invalida")
            
            return Statsnumber.pendente
    @staticmethod
    def verificar_expiracao(data_inicio:datetime):
        dias = (datetime.now()- data_inicio).days
        return dias > 15

