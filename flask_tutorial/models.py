"""
models.py
# Define o modelo ORM da tabela 'person' e o schema de serialização.
"""

from datetime import datetime
from config import db
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import auto_field

ma = Marshmallow()

class Person(db.Model):
    # Representa uma pessoa no banco de dados.
    __tablename__ = "person"

    person_id = db.Column(db.Integer, primary_key=True)
    lname     = db.Column(db.String(32), unique=True, nullable=False)
    fname     = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"<Person {self.fname} {self.lname}>"


class PersonSchema(ma.SQLAlchemyAutoSchema):
    # Serializa/deserializa objetos Person para/de JSON.
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session


# Instâncias reutilizáveis
person_schema  = PersonSchema()
people_schema  = PersonSchema(many=True)
