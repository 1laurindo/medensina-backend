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
    return "API MedEnsina Online"

@app.route('/aula', methods=['POST'])
def aula_interativa():
    data = request.json
    modulo = data.get("modulo")

    try:
        with open(f"prompts/{modulo}.json", "r", encoding="utf-8") as f:
            prompt_data = json.load(f)

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": prompt_data["system"]},
                {"role": "user", "content": prompt_data["user_prompt"]}
            ],
            temperature=0.8
        )

        return jsonify({"resposta": response['choices'][0]['message']['content']})

    except FileNotFoundError:
        return jsonify({"erro": "Módulo não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
