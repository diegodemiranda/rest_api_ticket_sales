""" 
app.py
Sistema de Venda de Ingressos Online
API REST com Flask + Connexion + SQLAlchemy + Marshmallow
"""

from flask import render_template
import connexion
from config import db
from models import Evento, Ingresso

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

flask_app = app.app
flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ingressos.db"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(flask_app)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    with flask_app.app_context():
        db.create_all()

        # Popula eventos de exemplo se o banco estiver vazio
        if not Evento.query.first():
            from datetime import datetime
            eventos = [
                Evento(
                    nome="Show Rock Nacional",
                    descricao="Os melhores clássicos do rock brasileiro",
                    local="Ginásio Municipal",
                    data_evento=datetime(2025, 8, 15, 20, 0),
                    preco=150.00,
                    capacidade=500,
                ),
                Evento(
                    nome="Festival de Jazz",
                    descricao="Jazz ao vivo com bandas nacionais e internacionais",
                    local="Teatro Municipal",
                    data_evento=datetime(2025, 9, 5, 19, 0),
                    preco=80.00,
                    capacidade=200,
                ),
                Evento(
                    nome="Peça de Teatro: Dom Casmurro",
                    descricao="Adaptação moderna do clássico de Machado de Assis",
                    local="Centro Cultural",
                    data_evento=datetime(2025, 7, 20, 18, 30),
                    preco=50.00,
                    capacidade=150,
                ),
            ]
            db.session.add_all(eventos)
            db.session.commit()
            print("Eventos de exemplo criados com sucesso.")

    app.run(host="0.0.0.0", port=8001, debug=True)
