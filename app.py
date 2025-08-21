from flask import Flask, jsonify, request
from database import db
from models.models import Refeicao
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:12345@127.0.0.1:3306/Diet_db'

db.init_app(app)

@app.route('/refeição', methods=['POST'])
def refeicao():
    data = request.json
    nome = data.get('nome')
    descricao = data.get('descricao')
    dataHora = datetime.datetime.now()

    if nome and descricao:
        refeicao = Refeicao(nome=nome, descricao=descricao, dataHora=dataHora)
        db.session.add(refeicao)
        db.session.commit()

    return jsonify({"message": "Refeição cadastrada com sucesso!"})

@app.route('/refeição/<int:id_ref>', methods=['GET'])
def read_refeicao(id_ref):
    
    refeicao = Refeicao.query.get(id_ref)

    if refeicao:
        return jsonify(refeicao.to_dict())
    return jsonify({'message': 'Objeto não encontrado'}), 404



if __name__ == '__main__':
    app.run(debug=True)