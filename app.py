from flask import Flask,jsonify

app = Flask(__name__)

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