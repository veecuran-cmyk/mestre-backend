# Arquivo: api/ia_master.py

from flask import Flask, request, jsonify
import requests
import os 
import json

app = Flask(__name__)

# 🚨 A CHAVE É LIDA AQUI, DE FORMA SEGURA, da Variável de Ambiente.
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
MODEL_NAME = "meta-llama/llama-3-8b-instruct:free"

@app.route('/ia_master', methods=['POST'])
def ia_master():
    # 1. Verifica a chave de segurança antes de qualquer coisa
    if not OPENROUTER_KEY:
        print("OPENROUTER_KEY não está configurada no servidor.")
        return jsonify({"error": "Chave API não configurada no servidor. Contate o administrador."}), 500

    try:
        data = request.json
        messages = data.get('messages', [])
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}", # Usa a chave SECRETA AQUI
            "Content-Type": "application/json",
            "HTTP-Referer": "https://mestreos.app",
            "X-Title": "MestreOS-Python-Backend"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": messages
        }
        
        # 2. Faz a chamada segura para o OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status() # Lança exceção em caso de erro HTTP (4xx ou 5xx)
        
        ai_response = response.json()
        
        # 3. Devolve SÓ o texto para o seu Front-end (o HTML)
        return jsonify({
            "text": ai_response["choices"][0]["message"]["content"]
        })

    except requests.exceptions.RequestException as e:
        # Erro de comunicação com a API externa
        print(f"Erro de API Externa: {e}")
        return jsonify({"error": "Erro de comunicação com a IA. Tente novamente."}), 500
    except Exception as e:
        # Erro interno
        print(f"Erro interno: {e}")
        return jsonify({"error": "Erro interno do servidor Python."}), 500