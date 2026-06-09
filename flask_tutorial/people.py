"""
people.py
Handlers chamados pelo Connexion conforme o operationId definido no swagger.yml.
"""

from datetime import datetime
from flask import abort, make_response
from config import db
from models import Person, person_schema, people_schema


# READ ALL  →  GET /api/people
def read_all():
    """Retorna lista com todas as pessoas."""
    pessoas = Person.query.order_by(Person.lname).all()
    return people_schema.dump(pessoas)



# CREATE  →  POST /api/people
def create(person):
    """Cria uma nova pessoa."""
    lname = person.get("lname")
    existente = Person.query.filter(Person.lname == lname).one_or_none()

    if existente:
        abort(406, f"Pessoa com sobrenome '{lname}' já existe.")

    nova_pessoa = person_schema.load(person)
    db.session.add(nova_pessoa)
    db.session.commit()
    return person_schema.dump(nova_pessoa), 201


# READ ONE  →  GET /api/people/{lname}
def read_one(lname):
    """Retorna uma pessoa pelo sobrenome."""
    pessoa = Person.query.filter(Person.lname == lname).one_or_none()

    if pessoa is None:
        abort(404, f"Pessoa com sobrenome '{lname}' não encontrada.")

    return person_schema.dump(pessoa)


# UPDATE  →  PUT /api/people/{lname}
def update(lname, person):
    """Atualiza uma pessoa existente."""
    existente = Person.query.filter(Person.lname == lname).one_or_none()

    if existente is None:
        abort(404, f"Pessoa com sobrenome '{lname}' não encontrada.")

    person["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    atualizada = person_schema.load(person, instance=existente)
    db.session.merge(atualizada)
    db.session.commit()
    return person_schema.dump(atualizada)


# DELETE  →  DELETE /api/people/{lname}
def delete(lname):
    """Remove uma pessoa pelo sobrenome."""
    existente = Person.query.filter(Person.lname == lname).one_or_none()

    if existente is None:
        abort(404, f"Pessoa com sobrenome '{lname}' não encontrada.")

    db.session.delete(existente)
    db.session.commit()
    return make_response(f"Pessoa '{lname}' removida com sucesso.", 200)
