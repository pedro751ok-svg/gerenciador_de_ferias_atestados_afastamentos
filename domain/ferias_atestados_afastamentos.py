from domain.constantes_de_status import Statsnumber
from datetime import datetime
class Atestado:
    @staticmethod
    def regras_atestado_medico(data_inicio, data_fim):

        days_ = (data_fim - data_inicio).days + 1

        if days_ > 15:
            return Statsnumber.encaminhado_afastamento
        else:
            return Statsnumber.pendente
class Afastamento_Inss:
    @staticmethod
    def afastado_pelo_inss():
        return Statsnumber.pendente
        
class Regras_ferias:
    @staticmethod
    def regas_ferias(data_inicio:int,data_fim:str):
        
        dias = (data_fim - data_inicio).days + 1

        if dias <= 0 :
            return "a data final deve ser maior que a data incio"
        if dias > 30:
            return "quantidade de dias invalida"
        return Statsnumber.pendente
    @staticmethod
    def vericar_expiracao(data_inicio):
        dias = (datetime.now()- data_inicio).days
        return dias > 15

