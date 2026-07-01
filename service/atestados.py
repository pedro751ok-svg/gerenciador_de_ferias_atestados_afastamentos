from models.dados_dos_funcionarios import Solicitacoes,session,Atestados_funcionarios
from domain.ferias_atestados_afastamentos import Atestado
class Atestados:
    @staticmethod
    def atestado_medico(id_solicitacao,data_inicio:int,data_fim:int):
                  
        with session() as sessao:
            solicitacao = sessao.query(Solicitacoes).filter_by(id=id_solicitacao).first()

            if not solicitacao:
                return "nenhuma solicitação feita"
            
            dias = (solicitacao.data_fim - solicitacao.data_inicio).days+ 1
            if not dias:
                return "acompanhamneto de data irregular"
            solicitacao.status = Atestado.regras_atestado_medico(data_fim=data_fim,data_inicio=data_inicio)
      
            sessao.commit()
        return solicitacao
    
    @staticmethod
    def gerenciar_cid(definir_cid:str,funcionario_id):
        with session() as sessao:
            funcionarios = sessao.query(Atestados_funcionarios).filter_by(id=funcionario_id).first()
            if not funcionarios:
                return "atestado nao existe "
            funcionarios.cid = definir_cid

            sessao.commit()