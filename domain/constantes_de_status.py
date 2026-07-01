import enum 
class Statsnumber(int,enum.Enum):
    pendente = 1
    aprovado = 2
    rejeitado = 3
    encaminhado_afastamento = 4
    
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

class StatusInss(str,enum.Enum):
    B31 = "Auxílio-doença comum"
    B91 = "Auxílio-doença acidente de trabalho"
    B94 = "Doença ocupacional"
    B92 = "Auxílio-acidente"