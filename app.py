from flask import Flask
from routes.end_point import rota
from models.dados_dos_funcionarios import Base, engine

app = Flask(__name__)


app.register_blueprint(rota)


if __name__ == "__main__":
    app.run(debug=True)