class Regrasdestatus:
    @staticmethod
    def status_regras(aprovado_por,rejeitado_por):
        if aprovado_por and rejeitado_por:
            raise ValueError("uma solicitacao nao pode possuir aprovador e reprovador ao mesmo tempo")