from backend.database.instance.database import db
from flask_login import UserMixin

class Administrador(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))  # Si usas contraseñas encriptadas, puedes cambiar esto más tarde
