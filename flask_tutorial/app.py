from flask import render_template
import connexion

from config import db
from models import Person

# Cria a aplicação via Connexion (que usa Flask internamente)
app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

# Configuração do banco SQLite 
flask_app = app.app
flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///people.db"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(flask_app)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    # Cria as tabelas se não existirem e popula com dados iniciais
    with flask_app.app_context():
        db.create_all()

        # Popula apenas se estiver vazio
        if not Person.query.first():
            from datetime import datetime
            pessoas_iniciais = [
                Person(fname="Tooth",  lname="Fairy",    timestamp=datetime(2022,10,8,9,15,10)),
                Person(fname="Knecht", lname="Ruprecht",  timestamp=datetime(2022,10,8,9,15,13)),
                Person(fname="Easter", lname="Bunny",     timestamp=datetime(2022,10,8,9,15,27)),
            ]
            db.session.add_all(pessoas_iniciais)
            db.session.commit()
            print("Banco populado com dados iniciais.")

    app.run(host="0.0.0.0", port=8000, debug=True)
