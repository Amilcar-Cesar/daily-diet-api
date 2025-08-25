from flask import Flask, jsonify, request
from database import db
from models.models import Refeicao, Usuario
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import datetime
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:12345@127.0.0.1:3306/Diet_db'

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userd_id):
    return Usuario.query.get(userd_id)

@app.route('/login', methods=['POST'])
def login():
   
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        user = Usuario.query.filter_by(username=username).first()
        
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Login realizado com sucesso!"})
    
    return jsonify({"message": "Falha no login."}), 401
    
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})


@app.route('/user/new_login', methods=['POST'])
def create_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        db.session.add(Usuario(username=username, password=hashed_password, role=role))
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso!"})
    return jsonify({"message": "Erro ao cadastrar usuário."}), 500

@login_required
@app.route('/user/<int:id_user>', methods=['GET'])
def read_user(id_user):
    user = Usuario.query.get(id_user)

    if user:
        return jsonify({
            'id': user.id,
            'username': user.username
        })
    return jsonify({'message': 'Objeto não encontrado'}), 404

@login_required
@app.route('/user/update/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    data = request.json
    user = Usuario.query.get(id_user)

    if current_user.id != id_user and current_user.role != 'admin':
        return jsonify({"message": "Ação não permitida."}), 403

    if user:
        user.password = data.get("password")
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Senha de usuário atualizada com sucesso!"})
    return jsonify({"message": "Erro ao atualizar senha."}), 500

@login_required
@app.route('/user/delete/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    user = Usuario.query.get(id_user)

    if current_user.id != id_user and current_user.role != 'admin':
        return jsonify({"message": "Ação não permitida."}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário removido com sucesso."})
    return jsonify({'message': 'Objeto não encontrado'}), 404

#----------------------------------------------------------------
#-------------------------------- Refeição ------------------------
#----------------------------------------------------------------

@login_required
@app.route('/refeição', methods=['POST'])
def create_refeicao():
    data = request.json
    nome = data.get('nome')
    descricao = data.get('descricao')
    dataHora = datetime.datetime.now()
    naDieta= data.get('naDieta')

    if nome and descricao:
        refeicao = Refeicao(nome=nome, descricao=descricao, dataHora=dataHora, naDieta=naDieta, autor=current_user)
        db.session.add(refeicao)
        db.session.commit()
        return jsonify({"message": "Refeição cadastrada com sucesso!"})
    return jsonify({"message": "Erro ao cadastrar dados."}), 500


@login_required
@app.route('/refeição/<int:id_ref>', methods=['GET'])
def read_refeicao(id_ref):
    
    refeicao = Refeicao.query.get(id_ref)
    
    if refeicao.autor.id != current_user.id:
        return jsonify({"message": "Ação não permitida."}), 403

    if refeicao:
        return jsonify(refeicao.to_dict())
    return jsonify({'message': 'Objeto não encontrado'}), 404


@login_required
@app.route('/refeição/lista', methods=['GET'])
def lista_refeicao():

    refeicoes_do_usuario = current_user.refeicoes
    return jsonify([refeicao.to_dict() for refeicao in refeicoes_do_usuario])


@login_required
@app.route('/refeição/editar/<int:id_ref>', methods=['PUT'])
def update_refeicao(id_ref):
    
    data = request.json
    refeicao = Refeicao.query.get(id_ref)
    
    if not refeicao:
        return jsonify({'message': 'Refeição não encontrada'}), 404
    
    if refeicao.autor.id != current_user.id:
        return jsonify({"message": "Ação não permitida."}), 403
    
    if 'nome' in data:
        refeicao.nome = data['nome']
    if 'descricao' in data:
        refeicao.descricao = data['descricao']
    if 'naDieta' in data:
        refeicao.naDieta = data['naDieta']
    
    
    refeicao.dataHora = datetime.datetime.now()
    db.session.commit()
    return jsonify({"message": "Refeição atualizada com sucesso!"})
    


@login_required
@app.route('/refeição/delete/<int:id_ref>', methods=['DELETE'])
def delete_refeicao(id_ref):
    
    refeicao = Refeicao.query.get(id_ref)

    if refeicao.autor.id != current_user.id:
        return jsonify({"message": "Ação não permitida."}), 403

    if refeicao:
        db.session.delete(refeicao)
        db.session.commit()
        return jsonify({"message": "Refeição removida com sucesso."})
    return jsonify({'message': 'Objeto não encontrado'}), 404




if __name__ == '__main__':
    app.run(debug=True)