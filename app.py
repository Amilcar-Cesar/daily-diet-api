from flask import Flask, jsonify
from database import db
from models.models import User
app = Flask(__name__)

app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:12345@127.0.0.1:3306/Diet_db'

db.init_app(app)

@app.route('/refeição', methods=['POST'])
def refeicao():
    refeicao = { 
        "Nome": "Nome de exemplo",
        "Descricao": "Descricao de exemplo",
        "Data": "data exemplo",
        "In diet": "sim/nao"
    }
    return jsonify(refeicao)



if __name__ == '__main__':
    app.run(debug=True)