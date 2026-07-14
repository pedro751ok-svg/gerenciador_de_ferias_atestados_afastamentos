# Gerenciador de Férias, Atestados e Afastamentos

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-black?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-black?logo=jsonwebtokens)
![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?logo=pytest&logoColor=white)

API REST desenvolvida em **Python**, **Flask** e **SQLAlchemy** para gerenciamento do ciclo completo de solicitações de férias, atestados médicos e afastamentos de funcionários.

O projeto implementa autenticação utilizando **JWT**, autorização baseada em papéis (**RBAC**), arquitetura em camadas e regras de negócio centralizadas, simulando um cenário corporativo de gestão de RH.

## Principais recursos

- Autenticação com JWT
- Controle de acesso baseado em papéis (RBAC)
- Arquitetura em Camadas
- SQLAlchemy ORM
- PostgreSQL
- Testes automatizados com Pytest
- Regras de negócio centralizadas

---

## Sumário

- [Visão geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Stack](#stack)
- [Modelo de dados](#modelo-de-dados)
- [Autenticação e permissões](#autenticação-e-permissões)
- [Como rodar](#como-rodar)
- [Endpoints da API](#endpoints-da-api)
- [Regras de negócio](#regras-de-negócio)
- [Testes](#testes)
- [Roadmap](#roadmap)

---

## Visão geral

Toda solicitação de ausência passa pela mesma entidade central (`Solicitacoes`), com um dado específico dependendo do tipo:

| Tipo | Descrição | Dado extra |
|---|---|---|
| Atestado | Afastamento médico comum | `cid` |
| Férias | Período de férias | — |
| Afastamento INSS | Auxílio-doença / acidente de trabalho | `codigo_especie` |

Cada solicitação nasce como `pendente` e segue um fluxo de aprovação com regras que impedem, por exemplo, aprovar e rejeitar ao mesmo tempo ou alterar uma solicitação já decidida.

---

## Arquitetura

Arquitetura em camadas, com responsabilidades isoladas:

```
Routes
   ↓
Middleware
   ↓
Controller
   ↓
Service
   ↓
Domain
   ↓
Models
```

| Camada | Responsabilidade |
|---|---|
| **Routes** | Define os endpoints e aplica os middlewares |
| **Middleware** | Valida token JWT e permissão (RBAC) |
| **Controller** | Extrai o payload, chama o service, formata a resposta |
| **Service** | Regras de negócio, validações, orquestração |
| **Domain** | Enums e regras centrais, independentes de infraestrutura |
| **Models** | Mapeamento SQLAlchemy das tabelas |

Essa separação permite testar cada camada isoladamente e trocar banco de dados ou formato de resposta sem tocar na lógica de negócio.

---

## Stack

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Framework web | Flask |
| ORM | SQLAlchemy |
| Autenticação | JWT (PyJWT) |
| Hash de senha | bcrypt |
| Banco de dados | PostgreSQL (produção) / SQLite (testes) |
| Variáveis de ambiente | python-dotenv |
| Testes | pytest |

---

## Modelo de dados

| Tabela | Campos principais |
|---|---|
| `funcionarios` | id, nome, email (único), cpf (único), senha (hash), role, setor, ativo |
| `tipo` | id, id_funcionario, descricao (`afastamento`\|`atestado`\|`ferias`), ativo |
| `solicitacoes` | id, id_funcionario, id_tipo, data_inicio, data_fim, status, aprovado_por, reprovado_por |
| `atestados` | id, id_solicitacao, cid |
| `afastamentos` | id, id_solicitacao, codigo_especie |
| `ferias` | id, id_solicitacao |

**Enums principais:** status da solicitação (`pendente`, `aprovado`, `rejeitado`, `cancelado`, `expirado`), roles (`ajudante`, `encarregado`, `gerente`, `rh`) e códigos INSS (`B31`, `B91`, `B92`, `B94`).

---

## Autenticação e permissões

**Autenticação:** login com `cpf` + `senha` → senha validada via hash bcrypt → token JWT gerado (`user_id`, `role`, expiração de 1h).

Rotas protegidas exigem:

```
Authorization: Bearer <token>
```

**Autorização (RBAC):** o `role` do funcionário é checado contra uma matriz de permissões antes de qualquer ação.

| Role | Permissões |
|---|---|
| `ajudante` | criar, cancelar e exibir a própria solicitação |
| `encarregado` | criar, cancelar, aceitar, rejeitar, exibir, gerenciar CID e afastamento |
| `gerente` | tudo do encarregado + gerenciar solicitações, histórico e pendências |
| `rh` | atualizar solicitações, cadastrar funcionários |

Sem a permissão exigida pela rota, a API responde `403`.

---

## Como rodar

```bash
git clone https://github.com/pedro751ok-svg/gerenciador_de_ferias_atestados_afastamentos.git
cd gerenciador_de_ferias_atestados_afastamentos

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Crie um `.env` na raiz do projeto:

```env
STK=sua_chave_secreta_para_assinar_o_jwt
URL_DATABASE=postgresql://usuario@localhost:5432/nome_do_banco
ALGORITIMO=HS256
```

```bash
python app.py
```

A API sobe em `http://127.0.0.1:5000`.

---

## Endpoints da API

Todas as rotas (exceto `/login`) exigem `Authorization: Bearer <token>` e a permissão correspondente.

| Método | Rota | Permissão | Descrição |
|---|---|---|---|
| POST | `/login` | — | Autentica e retorna o token JWT |
| POST | `/cadastro` | `rh` | Cadastra um funcionário |
| POST | `/tipo-solicitacao` | `criar_solicitacao` | Cria um tipo de solicitação |
| POST | `/gerenciador-solicitacoes` | `gerenciar_solicitacoes` | Cria uma solicitação (férias/atestado/afastamento) |
| POST | `/aceitar-solicitacao` | `aceitar_solicitacao` | Aprova uma solicitação pendente |
| POST | `/rejeitar-solicitacao` | `rejeitar_solicitacao` | Rejeita uma solicitação pendente |
| POST | `/cancelar-solicitacao` | `cancelar_solicitacao` | Cancela uma solicitação pendente |
| POST | `/atualizar-solicitacao` | `rh` | Atualiza uma solicitação pendente |
| PUT | `/gerenciar-cid` | `gerenciar_cid` | Atualiza o CID de um atestado |
| PUT | `/gerenciar-afastamentos-codigo_especie` | `gerenciar_afastamento` | Atualiza o código de espécie do INSS |
| GET | `/exibir-solicitacao` | `exibir_solicitacao` | Exibe uma solicitação |
| GET | `/exibir-historico-solicitacoes` | `gerente` | Histórico de solicitações |
| GET | `/exibir-solicitacoes-pendentes` | `gerente` | Lista solicitações pendentes |

**Exemplo — login:**

```json
POST /login
{
  "cpf": "00000000000",
  "senha": "senha123"
}
```

```json
200 OK
{
  "sucesso": "funcionario encontrado",
  "id_funcionario": 1,
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Exemplo — criar solicitação:**

```json
POST /gerenciador-solicitacoes
{
  "id_funcionario": 3,
  "id_tipo": 2,
  "data_inicio": "2026-08-01T00:00:00",
  "data_fim": "2026-08-10T00:00:00",
  "dados_extras": {
    "cid": "J11"
  }
}
```

> Para atestados, `dados_extras.cid` é obrigatório; para afastamentos INSS, utilize `dados_extras.codigo_especie`.

---

## Regras de negócio

- Toda solicitação nasce com status `pendente`.
- Um funcionário não pode possuir duas solicitações pendentes simultaneamente.
- `data_fim` nunca pode ser anterior a `data_inicio`.
- Apenas solicitações `pendentes` podem ser aprovadas, rejeitadas ou atualizadas.
- Uma solicitação não pode estar aprovada e rejeitada ao mesmo tempo (regra garantida na camada de domínio).
- Solicitações aprovadas não podem ser canceladas.
- Solicitações de férias passam por validações específicas antes da criação.
- Cada tipo de solicitação gera automaticamente seu respectivo registro especializado (`Ferias`, `Atestados` ou `Afastamentos`).

---

## Testes

Execute todos os testes:

```bash
pytest -v
```

A suíte utiliza **Pytest** com banco de dados isolado por execução através de fixtures definidas em `conftest.py`.

Os testes cobrem:

- Regras de negócio
- Validações de entrada
- Fluxos da aplicação
- Persistência utilizando SQLAlchemy

---

## Roadmap

- [ ] Documentação interativa (Swagger / OpenAPI)
- [ ] Paginação nas rotas de listagem
- [ ] Refresh Token
- [ ] Notificações automáticas de aprovação e rejeição
- [ ] Painel administrativo (Front-end)
- [ ] Docker / Docker Compose
- [ ] CI/CD (GitHub Actions)

---

## Licença

Este projeto ainda não possui uma licença formal.

Caso deseje utilizá-lo comercialmente ou redistribuí-lo, entre em contato com o autor.

---

<p align="center">
Desenvolvido em Python utilizando Flask, SQLAlchemy e PostgreSQL para demonstrar conceitos de autenticação JWT, RBAC, arquitetura em camadas e implementação de regras de negócio em aplicações backend.
</p>
