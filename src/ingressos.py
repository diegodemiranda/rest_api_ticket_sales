""" 
ingressos.py
Handlers para o recurso /ingressos (compra, listagem, cancelamento).
"""

from flask import abort, make_response
from config import db
from models import Evento, Ingresso, ingresso_schema, ingressos_schema


def read_all():
    # GET /api/ingressos — lista todas as compras (admin).
    todos = Ingresso.query.order_by(Ingresso.timestamp.desc()).all()
    return ingressos_schema.dump(todos)


def comprar(ingresso):
    """
    POST /api/ingressos — realiza a compra de ingresso(s).

    Regras de negócio:
      - O evento deve existir.
      - Quantidade mínima: 1; máxima por compra: 10.
      - Devem existir vagas suficientes.
      - Valor total é calculado automaticamente (preco × quantidade).
    """
    evento_id = ingresso.get("evento_id")
    quantidade = ingresso.get("quantidade", 1)

    # Validações
    if quantidade < 1 or quantidade > 10:
        abort(400, "Quantidade deve ser entre 1 e 10 por compra.")

    evento = Evento.query.get(evento_id)
    if evento is None:
        abort(404, f"Evento {evento_id} não encontrado.")

    if evento.vagas_disponiveis < quantidade:
        abort(409, f"Apenas {evento.vagas_disponiveis} vaga(s) disponível(is).")

    # Cria o ingresso com valor calculado
    novo_ingresso = Ingresso(
        evento_id=evento_id,
        nome_cliente=ingresso["nome_cliente"],
        email_cliente=ingresso["email_cliente"],
        cpf_cliente=ingresso["cpf_cliente"],
        quantidade=quantidade,
        valor_total=round(evento.preco * quantidade, 2),
        status="confirmado",
    )

    db.session.add(novo_ingresso)
    db.session.commit()
    return ingresso_schema.dump(novo_ingresso), 201


def read_one(ingresso_id):
    # GET /api/ingressos/{ingresso_id} — consulta um ingresso.
    ingresso = Ingresso.query.get(ingresso_id)
    if ingresso is None:
        abort(404, f"Ingresso {ingresso_id} não encontrado.")
    return ingresso_schema.dump(ingresso)


def cancelar(ingresso_id):
    # DELETE /api/ingressos/{ingresso_id} — cancela/remove um ingresso.
    ingresso = Ingresso.query.get(ingresso_id)
    if ingresso is None:
        abort(404, f"Ingresso {ingresso_id} não encontrado.")

    if ingresso.status == "cancelado":
        abort(409, f"Ingresso {ingresso_id} já está cancelado.")

    ingresso.status = "cancelado"
    db.session.commit()
    return make_response(f"Ingresso {ingresso_id} cancelado com sucesso.", 200)


def por_evento(evento_id):
    # GET /api/eventos/{evento_id}/ingressos — ingressos de um evento.
    evento = Evento.query.get(evento_id)
    if evento is None:
        abort(404, f"Evento {evento_id} não encontrado.")

    lista = Ingresso.query.filter_by(evento_id=evento_id).all()
    return ingressos_schema.dump(lista)
