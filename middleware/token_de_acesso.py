from service.jwt_token_acesso import Gerando_token,Validar_token
from flask import request,jsonify
from functools import wraps
def requer_token(funcao):
    @wraps(funcao)
    def decorated(*args , **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"erro":"token nao existente"}),401
        try:
            token = auth.split(" ")[1]
        except:
            return jsonify({"erro":"token invalido"})
        payload = Validar_token(token)
        if not payload:
            return jsonify({"erro":"token invalido ou expirado"})
        request.user_id = payload["user_id"]
        request.role = payload["role"]
        return funcao(*args,**kwargs)
    return decorated