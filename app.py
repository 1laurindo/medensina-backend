from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os
import json

load_dotenv()

app = Flask(__name__)
CORS(app) 

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/aula", methods=["POST"])
def aula():
    try:
        data = request.get_json()
        universidade = data.get("universidade", "")
        modulo = data.get("modulo", "")
        pergunta = data.get("pergunta", "")

        if not universidade or not modulo or not pergunta:
            return jsonify({"resposta": "Informações incompletas."}), 400

        prompt = f"Você é um professor da universidade {universidade}. No módulo {modulo}, o aluno perguntou: {pergunta}. Responda de forma didática e clara."

        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um professor inteligente e paciente."},
                {"role": "user", "content": prompt}
            ]
        )

        texto_resposta = resposta["choices"][0]["message"]["content"]
        return jsonify({"resposta": texto_resposta})

    except Exception as e:
        print("Erro:", e)
        return jsonify({"resposta": "Erro ao gerar resposta."}), 500

if __name__ == "__main__":
    app.run(debug=True)
