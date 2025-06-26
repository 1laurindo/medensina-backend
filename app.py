from flask_cors import CORS
CORS(app)
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os
import json

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "API MedCore IA Online"

@app.route('/aula', methods=['POST'])
def aula_interativa():
    data = request.json
    universidade = data.get("universidade")
    modulo = data.get("modulo")
    pergunta = data.get("pergunta")

    if not universidade or not modulo or not pergunta:
        return jsonify({"erro": "Parâmetros inválidos: envie universidade, modulo e pergunta"}), 400

    try:
        caminho_prompt = f"prompts/{universidade}/{modulo}.json"
        with open(caminho_prompt, "r", encoding="utf-8") as f:
            prompt_data = json.load(f)

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": prompt_data["system"]},
                {"role": "user", "content": prompt_data["user_prompt"] + "\n\nPergunta do aluno: " + pergunta}
            ],
            temperature=0.8
        )

        return jsonify({"resposta": response['choices'][0]['message']['content']})

    except FileNotFoundError:
        return jsonify({"erro": "Módulo ou universidade não encontrados"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
