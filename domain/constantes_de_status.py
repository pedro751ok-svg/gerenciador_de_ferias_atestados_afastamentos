import enum 

class DescricaoEnum(str,enum.Enum):
    afastamento = "afastamento"
    atestado = "atestado"
    ferias = "ferias"
    
class StatEnum(str,enum.Enum):
    pendente = "pendente"
    aprovado = "aprovado"
    rejeitado = "rejeitado"
    encaminhado_afastamento = "encaminhado_afastamento"
    cancelado = "cancelado"
    expirado = "expirado"

class Roleenum(str,enum.Enum):
    ajudante = "ajudante"
    encarregado = "encarregado"
    gerente = "gerente"
    rh = "rh"

class StatusInss(str,enum.Enum):
    B31 = "Auxílio-doença comum"
    B91 = "Auxílio-doença acidente de trabalho"
    B94 = "Doença ocupacional"
    B92 = "Auxílio-acidente"