import requests
from .audio_processing import convert_to_wav, clean_up
from .whisper_integration import transcribe_audio
from requests.auth import HTTPBasicAuth
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

def download_audio(media_url):
    try:
        response = requests.get(media_url)
        audio_path = 'audio_message.mp3'
        with open(audio_path, 'wb') as f:
            f.write(response.content)
        return audio_path
    except Exception as e:
        print(f"Erro ao tentar baixar o audio: {e}")
        raise

def process_incoming_message(media_url):
    audio_file = download_audio(media_url)
    wav_file = convert_to_wav(audio_file)
    text = transcribe_audio(wav_file)
    clean_up([audio_file, wav_file])
    return text
