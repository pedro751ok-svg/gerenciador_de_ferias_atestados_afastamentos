import jwt
from dotenv import load_dotenv
from datetime import datetime,timezone,timedelta
load_dotenv()
import os 
senha = os.getenv("SENHA_TOKEN")
class Gerando_token:
    @staticmethod
    def gerar(usuario_id):
        
        payload = {
            "user_id":usuario_id,
            "exp":datetime.now(timezone.utc)+ timedelta(hours=1)
        }

        token = jwt.encode(payload,senha,algorithm="HS256")

        return token
class Validar_token:
    @staticmethod
    def validar_token(token):
        try:
            payload = jwt.decode(
                token,
                senha,
                algorithms = "HS256"
            )
            return payload
        except jwt.ExpiredSignatureError:
            return "erro token invalido"
        except jwt.InvalidTokenError:
            return "token invalido"
token = Gerando_token.gerar(1)
print("Token gerado:", token)

payload = Gerando_token.validar_token(token)
print("Payload:", payload)