import whisper

# Carregar o modelo Whisper
model = whisper.load_model("small")  # ou "small", "medium", "large"

def transcribe_audio(audio_file):
    """Transcribe the audio file using Whisper locally."""
    # Carregar o áudio
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    # Fazer a transcrição
    result = model.transcribe(audio)

    return result['text']
