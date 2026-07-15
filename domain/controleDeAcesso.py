class ControleAcesso:

    PERMISSOES = {
        "funcionario": [
            "criar_solicitacao",
            "cancelar_solicitacao",
            "exibir_solicitacao"
            
        ],

        "encarregado": [
            "criar_solicitacao",
            "cancelar_solicitacao",
            "aceitar_solicitacao",
            "rejeitar_solicitacao",
            "exibir_solicitacao",
            "gerenciar_cid",
            "gerenciar_afastamento"
            
        ],

        "gerente": [
            "criar_solicitacao",
            "cancelar_solicitacao",
            "aceitar_solicitacao",
            "rejeitar_solicitacao",
            "gerenciar_solicitacoes",
            "historico_solicitacoes",
            "listar_solicitacoes_pendentes",
            "exibir_solicitacao",
            "gerenciar_cid",
            "gerenciar_afastamento"
        ],
        "rh":[
            "listar_solicitacoes_pendentes",
            "historico_solicitacoes",
            "aceitar_solicitacao",
            "rejeitar_solicitacao"  
        ]
    }
    @staticmethod
    def controle_de_acesso(role, permissao):
        return permissao in ControleAcesso.PERMISSOES.get(role, [])
