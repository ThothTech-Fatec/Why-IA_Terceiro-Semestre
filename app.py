import os
import time
from flask import Flask, request
import requests
from config import TELEGRAM_BOT_TOKEN
from utils.whatsapp import process_incoming_message
from iallama import OllamaQuestion, gerar_audio
from testeRAG import OllamaQ

app = Flask(__name__)

# Configuração do Telegram
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"



def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url, data=payload)
    return response

def send_audio_message(chat_id, audio_file_path):
    """Função para enviar um áudio MP3 como mensagem."""
    url = f"{TELEGRAM_API_URL}/sendAudio"
    payload = {
        'chat_id': chat_id,
    }
    files = {
        'audio': open(audio_file_path, 'rb')  # Carrega o arquivo MP3
    }
    response = requests.post(url, data=payload, files=files)
    return response.json()

def create_reply_markup():
    """Cria os botões para o usuário escolher entre texto ou áudio."""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Texto", "callback_data": "text"},
                {"text": "Áudio", "callback_data": "audio"}
            ]
        ]
    }
    return keyboard

user_choices = {}  # Armazena a escolha do usuário (texto ou áudio)

@app.route('/webhook', methods=['POST'])
def webhook():
    chat_id = None
    try:
        data = request.json
        print("Dados recebidos:", data)

        if 'message' in data:
            chat_id = data['message']['chat']['id']
            incoming_msg = data['message'].get('text', '').lower()
            voice_message = data['message'].get('voice')
            audio_message = data['message'].get('audio')

            if incoming_msg == "/texto":
                # Ativa quando o usuario escolher texto
                user_choices[chat_id] = "text"
                send_telegram_message(chat_id, "Você escolheu: Texto. Agora envie sua pergunta.")
                return "OK"

            elif incoming_msg == "/audio":
                # O usuário escolheu 'Áudio'
                user_choices[chat_id] = "audio"
                send_telegram_message(chat_id, "Você escolheu: Áudio. Agora envie sua pergunta.")
                return "OK"

            elif 'callback_query' in data:
                # Para alternar com os botões inline
                callback_data = data['callback_query']['data']
                user_choices[chat_id] = callback_data  # Armazena a escolha do usuário
                send_telegram_message(chat_id, f"Você escolheu: {callback_data.capitalize()}. Agora envie sua pergunta.")
                return "OK"

            if voice_message or audio_message:
                # Caso tenha um arquivo de áudio ou voz
                file_id = voice_message['file_id'] if voice_message else audio_message['file_id']
                file_info = requests.get(f"{TELEGRAM_API_URL}/getFile?file_id={file_id}").json()
                file_path = file_info['result']['file_path']
                download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"

                # Baixa, converte e transcreve o áudio
                text = process_incoming_message(download_url)
                send_telegram_message(chat_id, "Transcrevendo o áudio...")

                # Resposta da IA para o texto transcrito
                response_text = OllamaQuestion(text)

                # Verifica a escolha do usuário
                response_format = user_choices.get(chat_id, 'text')  # 'text' é o valor padrão
                if response_format == 'audio':
                    # Converte o texto para áudio
                    audio_file_path = gerar_audio(response_text)
                    send_audio_message(chat_id, audio_file_path)  # Envia o áudio para o usuário
                else:
                    send_telegram_message(chat_id, response_text)  # Envia a resposta em texto

            else:
                # Caso seja uma mensagem de texto
                response_text = OllamaQuestion(incoming_msg)  # Processa o texto do usuário

                # Verifica a escolha do usuário
                response_format = user_choices.get(chat_id, 'text')  # 'text' é o valor padrão
                if response_format == 'audio':
                    # Converte o texto para áudio
                    audio_file_path = gerar_audio(response_text)
                    send_audio_message(chat_id, audio_file_path)  # Envia o áudio para o usuário
                else:
                    send_telegram_message(chat_id, response_text)  # Envia a resposta em texto

            return "OK"

        else:
            print("Estrutura do JSON inválida. Campo 'message' ou 'chat' ausente.")
            if chat_id:
                send_telegram_message(chat_id, "Erro: Estrutura da mensagem não é suportada.")
            return "Erro na estrutura da mensagem", 400

    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
        if chat_id:
            send_telegram_message(chat_id, "Erro interno do servidor.")
        return "Erro", 500




@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        chat_id = request.form['chat_id']
        message_body = request.form['body']
        
        # Envia mensagem inicial para o usuário

        response_ai = OllamaQuestion(message_body)
        if response_ai:
            send_telegram_message(chat_id, response_ai)
        else:
            print("Resposta da IA vazia, não enviando mensagem.")

        return "Mensagem enviada com sucesso!"
    except Exception as e:
        print(f"Error sending message: {e}")
        return "Erro ao enviar mensagem.", 500
    
if __name__ == '__main__':
    app.run(debug=True)
