from flask import Flask
from routes.end_point import rota
from models.dados_dos_funcionarios import Base, engine
from extensoes import limiter

Base.metadata.create_all(engine)
app = Flask(__name__)

limiter.init_app(app)

app.register_blueprint(rota)

if __name__ == "__main__":
    app.run(debug=False)