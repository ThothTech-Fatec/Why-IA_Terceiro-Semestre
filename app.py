import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from utils.whatsapp import process_incoming_message
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
app = Flask(__name__)

# Configurações do Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        incoming_msg = request.values.get('Body', '').lower()
        media_url = request.values.get('MediaUrl0', None)

        response = MessagingResponse()
        msg = response.message()

        if media_url:
            text = process_incoming_message(media_url)
            msg.body(text)
        else:
            msg.body("Envie Apenas mensagens em voz.")

        return str(response)
    except Exception as e:
        print(f"Error in webhook: {e}")
        response = MessagingResponse()
        response.message("Erro interno do servidor.")
        return str(response), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
     
        to_number = request.form['to']  
        message_body = request.form['body'] 
        
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,  
            body=message_body,
            to=f'whatsapp:{to_number}'
        )
        return f"Mensagem enviada com sucesso! SID: {message.sid}"
    except Exception as e:
        print(f"Error sending message: {e}")
        return "Erro ao enviar mensagem.", 500

if __name__ == '__main__':
    app.run(debug=True)
