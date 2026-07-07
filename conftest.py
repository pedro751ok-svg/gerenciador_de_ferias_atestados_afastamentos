import pytest
from database.banco_de_testes import session_teste,engine 

@pytest.fixture()
def db_test():
    conection = engine.connect()
    transacao = conection.begin()
    session = session_teste(bind =conection)
    yield session

    session.close()
    transacao.rollback()
    conection.close()