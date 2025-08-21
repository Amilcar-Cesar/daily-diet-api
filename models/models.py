from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    dataHora = db.Column(db.DateTime, nullable=False)
    naDieta = db.Column(db.String(),nullabe=True, default=True)