"""
eventos.py
Handlers para o recurso /eventos (CRUD completo).
"""

from flask import abort, make_response
from config import db
from models import Evento, evento_schema, eventos_schema


def read_all():
    # GET /api/eventos — lista todos os eventos.
    eventos = Evento.query.order_by(Evento.data_evento).all()
    resultado = []
    for e in eventos:
        dados = evento_schema.dump(e)
        dados["ingressos_vendidos"] = e.ingressos_vendidos
        dados["vagas_disponiveis"]  = e.vagas_disponiveis
        resultado.append(dados)
    return resultado


def create(evento):
    # POST /api/eventos — cria um novo evento.
    nome = evento.get("nome")
    if Evento.query.filter(Evento.nome == nome).first():
        abort(406, f"Evento '{nome}' já existe.")

    novo = evento_schema.load(evento)
    db.session.add(novo)
    db.session.commit()

    dados = evento_schema.dump(novo)
    dados["ingressos_vendidos"] = novo.ingressos_vendidos
    dados["vagas_disponiveis"]  = novo.vagas_disponiveis
    return dados, 201


def read_one(evento_id):
    # GET /api/eventos/{evento_id} — detalhes de um evento.
    evento = Evento.query.get(evento_id)
    if evento is None:
        abort(404, f"Evento {evento_id} não encontrado.")

    dados = evento_schema.dump(evento)
    dados["ingressos_vendidos"] = evento.ingressos_vendidos
    dados["vagas_disponiveis"]  = evento.vagas_disponiveis
    return dados


def update(evento_id, evento):
    # PUT /api/eventos/{evento_id} — atualiza um evento.
    existente = Evento.query.get(evento_id)
    if existente is None:
        abort(404, f"Evento {evento_id} não encontrado.")

    atualizado = evento_schema.load(evento, instance=existente)
    db.session.commit()

    dados = evento_schema.dump(atualizado)
    dados["ingressos_vendidos"] = atualizado.ingressos_vendidos
    dados["vagas_disponiveis"]  = atualizado.vagas_disponiveis
    return dados


def delete(evento_id):
    # DELETE /api/eventos/{evento_id} — remove um evento.
    existente = Evento.query.get(evento_id)
    if existente is None:
        abort(404, f"Evento {evento_id} não encontrado.")

    db.session.delete(existente)
    db.session.commit()
    return make_response(f"Evento {evento_id} removido com sucesso.", 200)
