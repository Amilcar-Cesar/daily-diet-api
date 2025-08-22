from flask import Flask, jsonify, request
from database import db
from models.models import Refeicao
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:12345@127.0.0.1:3306/Diet_db'

db.init_app(app)

@app.route('/refeição', methods=['POST'])
def create_refeicao():
    data = request.json
    nome = data.get('nome')
    descricao = data.get('descricao')
    dataHora = datetime.datetime.now()
    naDieta= data.get('naDieta')

    if nome and descricao:
        refeicao = Refeicao(nome=nome, descricao=descricao, dataHora=dataHora, naDieta=naDieta)
        db.session.add(refeicao)
        db.session.commit()
        return jsonify({"message": "Refeição cadastrada com sucesso!"})
    return jsonify({"message": "Erro ao cadastrar dados."}), 500


@app.route('/refeição/<int:id_ref>', methods=['GET'])
def read_refeicao(id_ref):
    
    refeicao = Refeicao.query.get(id_ref)

    if refeicao:
        return jsonify(refeicao.to_dict())
    return jsonify({'message': 'Objeto não encontrado'}), 404


@app.route('/refeição/lista', methods=['GET'])
def lista_refeicao():

    refeicoes = Refeicao.query.all()
    return jsonify([refeicao.to_dict() for refeicao in refeicoes])


@app.route('/refeição/editar/<int:id_ref>', methods=['PUT'])
def update_refeicao(id_ref):
    
    data = request.json
    refeicao = Refeicao.query.get(id_ref)
    
    if refeicao:
        refeicao.nome = data.get("nome")
        refeicao.descricao = data.get("descricao")
        refeicao.naDieta = data.get("naDieta")
        db.session.add(refeicao)
        db.session.commit()
        return jsonify({"message": "Refeição atualizada com sucesso!"})
    return jsonify({"message": "Erro ao atualizar dados."}), 500


@app.route('/refeição/delete/<int:id_ref>', methods=['DELETE'])
def delete_refeicao(id_ref):
    
    refeicao = Refeicao.query.get(id_ref)

    if refeicao:
        db.session.delete(refeicao)
        db.session.commit()
        return jsonify({"message": "Refeição removida com sucesso."})
    return jsonify({'message': 'Objeto não encontrado'}), 404




if __name__ == '__main__':
    app.run(debug=True)