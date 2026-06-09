"""
models.py
Modelos ORM e schemas Marshmallow para o sistema de ingressos.
"""

from datetime import datetime
from config import db
from flask_marshmallow import Marshmallow
import marshmallow as ma_core

ma = Marshmallow()



# MODELOS
class Evento(db.Model):
    # Representa um evento disponível para venda de ingressos.
    __tablename__ = "evento"

    evento_id   = db.Column(db.Integer, primary_key=True)
    nome        = db.Column(db.String(120), nullable=False)
    descricao   = db.Column(db.String(500))
    local       = db.Column(db.String(120))
    data_evento = db.Column(db.DateTime, nullable=False)
    preco       = db.Column(db.Float, nullable=False)
    capacidade  = db.Column(db.Integer, nullable=False)

    # Relacionamento: um evento possui vários ingressos
    ingressos = db.relationship(
        "Ingresso",
        backref="evento",
        cascade="all, delete-orphan",
        lazy=True,
    )

    @property
    def ingressos_vendidos(self):
        return Ingresso.query.filter_by(evento_id=self.evento_id).count()

    @property
    def vagas_disponiveis(self):
        return self.capacidade - self.ingressos_vendidos

    def __repr__(self):
        return f"<Evento {self.nome}>"


class Ingresso(db.Model):
    # Representa a compra de um ingresso por um cliente.
    __tablename__ = "ingresso"

    ingresso_id   = db.Column(db.Integer, primary_key=True)
    evento_id     = db.Column(db.Integer, db.ForeignKey("evento.evento_id"), nullable=False)
    nome_cliente  = db.Column(db.String(100), nullable=False)
    email_cliente = db.Column(db.String(120), nullable=False)
    cpf_cliente   = db.Column(db.String(14), nullable=False)
    quantidade    = db.Column(db.Integer, nullable=False, default=1)
    valor_total   = db.Column(db.Float, nullable=False)
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow)
    status        = db.Column(db.String(20), default="confirmado")

    def __repr__(self):
        return f"<Ingresso {self.ingresso_id} - {self.nome_cliente}>"


# SCHEMAS (serialização com Marshmallow)
class EventoSchema(ma.SQLAlchemyAutoSchema):
    # Serializa Evento para JSON; campos calculados adicionados manualmente.
    class Meta:
        model = Evento
        load_instance = True
        sqla_session = db.session
        # Exclui o relacionamento (não é coluna SQL)
        exclude = ("ingressos",)


class IngressoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingresso
        load_instance = True
        sqla_session = db.session
        include_fk = True


# Instâncias reutilizáveis
evento_schema    = EventoSchema()
eventos_schema   = EventoSchema(many=True)
ingresso_schema  = IngressoSchema()
ingressos_schema = IngressoSchema(many=True)
