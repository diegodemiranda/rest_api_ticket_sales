"""
config.py
Instância compartilhada do SQLAlchemy.
Criada aqui para evitar importações circulares entre app.py e models.py.
""" 

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
