from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os
import json
import traceback

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/aula", methods=["POST"])
def aula():
    try:
        data = request.get_json()
        universidade = data.get("universidade")
        modulo = data.get("modulo")

        prompt_base = f"Você é um professor interativo. Dê as boas-vindas ao aluno no módulo {modulo} da universidade {universidade}. Seja gentil, didático e convide o aluno a tirar dúvidas."

        response = openai.ChatCompletion.create(
            model="gpt-4",  # ou "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt_base}]
        )

        resposta = response.choices[0].message["content"]
        return jsonify({"resposta": resposta})

    except Exception as e:
        print("Erro:", traceback.format_exc())
        return jsonify({"erro": "Não foi possível iniciar a aula"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
