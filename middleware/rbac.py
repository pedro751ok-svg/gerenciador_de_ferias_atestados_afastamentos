from functools import wraps
from flask import request,jsonify
from domain.controleDeAcesso import ControleAcesso
def requer_permissao(permissao):
    def decorador(func):
        @wraps (func)
        def wrarper(*args,**kwargs):
            role =- request.role
            if not ControleAcesso.controle_de_acesso(role,permissao):
                return jsonify({"erro":"acesso negado"}),403
            return func(*args,**kwargs)
        return wrarper
    return decorador