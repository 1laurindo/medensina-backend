from flask import Flask, request, jsonify
from flask_cors import cross_origin
from dotenv import load_dotenv
import openai
import os
import traceback

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/aula", methods=["POST"])
@cross_origin(origins="*")  # LIBERA o frontend para acessar
def aula():
    try:
        data = request.get_json()
        universidade = data.get("universidade")
        modulo = data.get("modulo")
        pergunta = data.get("pergunta", "")

        if pergunta == "introducao":
            prompt_base = (
                f"Você é um professor interativo chamado Professor Core. "
                f"Dê as boas-vindas ao aluno que escolheu o módulo '{modulo}' na universidade '{universidade}'. "
                "Seja gentil, acolhedor e didático. Explique o que será abordado nesse módulo de forma empolgante. "
                "Convide o aluno a fazer perguntas para aprofundar ainda mais seu aprendizado."
            )
        else:
            prompt_base = (
                f"Você é o Professor Core, um assistente educacional interativo. "
                f"Responda de forma clara, prática e acolhedora à pergunta do aluno sobre o módulo '{modulo}' da universidade '{universidade}'. "
                f"Pergunta: {pergunta}"
            )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt_base}]
        )

        resposta = response.choices[0].message["content"]
        return jsonify({"resposta": resposta})

    except Exception as e:
        print("Erro:", traceback.format_exc())
        return jsonify({"erro": "Não foi possível iniciar a aula"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
