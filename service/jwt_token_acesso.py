import jwt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from config.configurações import conf_priv
from models.dados_dos_funcionarios import Funcionarios

load_dotenv()

import os 

senha = os.getenv(conf_priv.STK)


class Gerando_token:

    @staticmethod
    def gerar(funcionario):

        payload = {
            "user_id": funcionario.id,
            "role": funcionario.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }

        token = jwt.encode(
            payload,
            senha,
            algorithm=conf_priv.ALGORITHM
        )

        return token


class Validar_token:

    @staticmethod
    def validar_token(token):

        try:
            payload = jwt.decode(
                token,
                senha,
                algorithms=[conf_priv.ALGORITHM]  
    
            )

            return payload

        except jwt.ExpiredSignatureError:
            return "erro token invalido"

        except jwt.InvalidTokenError:
            return "token invalido"
