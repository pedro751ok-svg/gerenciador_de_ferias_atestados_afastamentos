from flask import request,jsonify
from service.afastamento import AfastamentoValidador
from service.atestados import AtestadoValidador
from service.Controle_De_AcessoEStatus import SolicitacoesServices
from service.ferias import FeriasValidador
from service.jwt_token_acesso import Gerando_token
from service.logins import Cadastro_e_login
from service.solicitacoes import Solicitacao_service
from models.dados_dos_funcionarios import session
class ControleGeral:
    @staticmethod
    def controlle_afastamentos():
            dados = request.get_json()

            id_solicitacao = dados.get("id_solicitacao")
            tipo_de_solicitacao = dados.get("tipo_de_solicitacao")
            codigo_especie = dados.get("codigo_especie")
            try:

                with session() as db:
                    funcionario = AfastamentoValidador.gerenciar_afastamento(
                        id_solicitacao=id_solicitacao,
                        tipo_de_solicitacao=tipo_de_solicitacao,
                        codigo_especie=codigo_especie,
                        db=db
                    )
                    db.commit()

                    return jsonify({"sucesso":"afastamento atualizado com sucesso",
                                "id_solicitacao":funcionario.id_solicitacao,
                                "tipo_de_solicitacao":funcionario.codigo_especie}),200
        
            except Exception as e:
                    db.rollback()
                    return jsonify({"erro":str(e)}),400
            
    @staticmethod
    def controlle_atestados():
        dados = request.get_json()
        id_solicitacao = dados.get("id_solicitacao")
        cid = dados.get("cid")
        try:
              
            with session() as db:
                    funcionario = AtestadoValidador.definir_cid(
                        id_solicitacao=id_solicitacao,
                        cid = cid,
                        db = db
                        )
                    db.commit()
                    return jsonify({"sucesso":"cid atualizado com sucesso",
                                    "id_solicitacao":funcionario.id}),200
        
        except Exception as e:
                db.rollback()
                return jsonify({"erro":str(e)}),400
        
    @staticmethod
    def controlle_de_cadastros():
        dados = request.get_json()
        nome = dados.get("nome")
        email = dados.get("email")
        cpf = dados.get("cpf")
        senha = dados.get("senha")
        role = dados.get("role")
        setor = dados.get("setor")
        ativo = dados.get("ativo")

        try:
            
            with session() as db:
                novo_funcionario = Cadastro_e_login.cadastro_de_usuario(
                    nome=nome,
                    email=email,
                    cpf=cpf,
                    senha=senha,
                    role=role,
                    setor=setor,
                    ativo=ativo,
                    db = db
                )
                db.commit()
                return jsonify({"sucesso":"cadastrado com sucesso",
                                "id funcionario":novo_funcionario.id,
                                "nome":novo_funcionario.nome,
                                "role":novo_funcionario.role}),200
        except Exception as e:
      
            return jsonify({"erro":str(e)}),400
        
    @staticmethod
    def controlle_de_logins():
        dados = request.get_json()
        cpf = dados.get("cpf")
        senha = dados.get("senha")
        try:
            
            with session() as db:
                funcionario = Cadastro_e_login.login_funcionario(
                    cpf=cpf,
                    senha=senha,
                    db = db
                )
                token = Gerando_token.gerar(funcionario)
                return jsonify({"sucesso":"funcionario encontrado",
                                "id_funcionario":funcionario.id,
                                "token":token}),200

        except Exception as e:
            
            return jsonify({"erro":str(e)}),400
        
    @staticmethod
    def controlle_tipo_de_solicitacao():
        dados = request.get_json()

        descricao = dados.get("descricao")
        ativo = dados.get("ativo")
        try:
            
            with session() as db:
                solicitacao = Solicitacao_service.tipo_de_solicitacao(
                    descricao=descricao,
                    ativo=ativo,
                    db = db
                )
                return jsonify({"sucesso":"solicitacao enviada para analise com sucesso",
                                "id da solicitacao":solicitacao.id}),200

        except Exception as e:
               
                return jsonify({"erro":str(e)}),400
        
    @staticmethod
    def controlle_gerenciador_de_solicitacoes():
        dados = request.get_json()

        data_inicio = dados.get("data_incio")
        data_fim = dados.get("data_fim")
        id_funcionario = dados.get("id_funcionario")
        id_tipo = dados.get("id_tipo")
        dados_extras = dados.get("dados_extras")
        try:
            
            with session() as db:
                gerenciador = Solicitacao_service.gerenciador_solicitacoes(
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    id_funcionario=id_funcionario,
                    id_tipo=id_tipo,
                    dados_extras=dados_extras,
                    db = db
                )
                return jsonify({"sucesso":"solicitacao criada com sucesso",
                                "id_solicitacao":gerenciador.id,
                                "status_atual":gerenciador.status}),200

        except Exception as e:
            
            return jsonify({"erro": str(e)}),400
        
    @staticmethod
    def controlle_exibir_solicitacao():
        dados = request.get_json()

        id_solicitacao = dados.get("id_solicitacao")
        try:
            with session() as db:
                solicitacao = Solicitacao_service.exibir_solicitacao(
                    id_solicitacao=id_solicitacao,
                    db=db
                )
                return jsonify({"resultado":solicitacao}),200
        except Exception as e:
            return jsonify({"erro":str(e)}),400
        
    @staticmethod
    def controlle_aceitar_solicitacoes():
        dados = request.get_json()
        id_solicitacao = dados.get("id_solicitacao")
        aprovado_por = dados.get("aprovado_por")

        try:
           
            with session() as db:
                Solicitacao = Solicitacao_service.aceitar_solicitacao(
                    id_solicitacao=id_solicitacao,
                    aprovado_por=aprovado_por,
                    db= db
                )
                db.commit()
                return jsonify({"sucesso":"solicitacao aceita",
                                "id da solicitacao":Solicitacao.id,
                                "aprovado por":Solicitacao.aprovado_por}),200

        except Exception as e:
           
            return jsonify({"erro":str(e)}),400
        
    @staticmethod
    def controlle_rejeitar_solicitacao():
        dados = request.get_json()

        id_solicitacao = dados.get("id_solicitacao")
        reprovado_por = dados.get("reprovado_por")
        try:
           
            with session() as db:
                solicitacao = Solicitacao_service.rejeitar_solicitacao(
                    id_solicitacao=id_solicitacao,
                    reprovado_por=reprovado_por,
                    db=db
                )
                db.commit()
                return jsonify({"sucesso":"solicitacao cancelada com sucesso",
                                "id da solicitacao":solicitacao.id,
                                "reprovada por":solicitacao.reprovado_por}),200

        except Exception as e:

            return jsonify({"erro":str (e)}),400
        
    @staticmethod
    def controlle_historico_de_solicitacoes():
        dados = request.get_json()
        id_solicitacao = dados.get("id_solicitacao")
        try:
            with session() as db:
                solicitacao = Solicitacao_service.historico_solicitacoes(
                    id_solicitacao=id_solicitacao,
                    db=db
                )
                return jsonify({"resultado todas solicitacoes":solicitacao}),200
        except Exception as e:
            return jsonify({"erro":str(e)}),400
        
    @staticmethod
    def controlle_cancelar_solicitacoes():
        dados = request.get_json()
        id_solicitacao = dados.get("id_solicitacao")
        try:
            
            with session() as db:
                solicitacao = Solicitacao_service.cancelar_solicitacao(
                    id_solicitacao=id_solicitacao,
                    db=db
                )
                db.commit()
                return jsonify({"sucesso":"solicitacao cancelada com sucesso",
                                "id_solicitacao":solicitacao.id,
                                "status da solicitacao":solicitacao.status}),200

        except Exception as e:
         
            return jsonify({"erro":str(e)}),400
        
    @staticmethod
    def controlle_solicitacoes_pendentes():
        solicitacao_status = request.args.get("status")
        try:
            resultado = Solicitacao_service.listar_solicitações_pendentes(solicitacao_status=solicitacao_status)
            if isinstance (resultado ,str):
                return jsonify({"sucesso":resultado}),200
            lista = [{
                "id": s.id,
                "id_funcionario": s.id_funcionario,
                "id_tipo": s.id_tipo,
                "data_inicio": s.data_inicio,
                "data_fim": s.data_fim,
                "status": s.status,
            }
            for s in resultado
            ]
            return jsonify({"solicitacoes":lista}),200
        except Exception as e:
            return jsonify({"erro":str(e)}),400
        
    def controlle_atualizar_solicitacoes():
        dados = request.get_json()
        id_solicitacao = dados.get("id_solicitacao")
        id_tipo = dados.get("id_tipo")
        data_inicio = dados.get("data_inicio")
        data_fim = dados.get("data_fim")
        try:
           
            with session() as db:
                solicitacao = Solicitacao_service.atualizar_solicitacao(
                    id_solicitacao=id_solicitacao,
                    id_tipo=id_tipo,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    db=db
                )
                db.commit()
                return jsonify({"sucesso":"solicitacao atualizada com sucesso",
                                "consultar atualizacoes":solicitacao.id_solicitacao}),200

        except Exception as e:
    
            return jsonify({"erro":str(e)}),400