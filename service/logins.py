from models.dados_dos_funcionarios import Funcionarios,session
from utils.configurações_cpf_senhas import Gerenciador_cpf,Senha_hash
class Cadastro_e_login:
    
    @staticmethod
    def cadastro_de_usuario(cpf:str,nome:str,email:str,senha:str,role:str,setor:str,ativo:bool,db=None):
        if db is None:
            db = session()
            close_db = True
        else:
            close_db = False
    
            if not  Gerenciador_cpf.validar_cpf(cpf):
                raise ValueError ("cpf invalido")

            existe = db.query(Funcionarios).filter_by(cpf=cpf).first()
            if existe:
                raise ValueError("usuario ja cadastrado")
            senha_ok = Senha_hash.senha_hash(senha)
        try:
            funcionario = Funcionarios(
                nome=nome,
                email=email,
                cpf=cpf,
                senha=senha_ok,
                role=role,
                setor=setor,
                ativo=ativo
            )
            db.add(funcionario)
            db.commit()
            return funcionario
        except Exception as e:
            db.rollback()
            return f"erro de {e}"
        finally:
            if close_db:
                db.close()
    @staticmethod
    def login_funcionario(cpf:str,senha:str,db = None):
        if db is None:
            db = session()
            close_db = True
        else:
            close_db = False
        try:
            funcionario = db.query(Funcionarios).filter_by(cpf=cpf).first()
            
            if not funcionario:
                return "funcionario nao existe"
            
            senha_valida = Senha_hash.validar_senha(senha,funcionario.senha)

            if not senha_valida:
                return "senha invalida tente novamente"
            
  
            return funcionario
        finally:
            if close_db:
                db.close()

    @staticmethod
    def perfil_funcionario(user_id:int):
        with session() as sessao:
            funcionario = sessao.query(Funcionarios).filter_by(id=user_id).first()

            if not funcionario:
                return "funcionario nao existe ou esta inativo"
            
            return funcionario
        