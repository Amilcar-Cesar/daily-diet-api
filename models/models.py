from database import db
from flask_login import UserMixin

class Refeicao(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text(), nullable=False)
    dataHora = db.Column(db.DateTime, nullable=False)
    naDieta = db.Column(db.String(30),nullable=True, default='sim')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'dataHora': self.dataHora.strftime('%d/%m/%Y %H:%M') if self.dataHora else None,
            'naDieta': self.naDieta
        }
    
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')