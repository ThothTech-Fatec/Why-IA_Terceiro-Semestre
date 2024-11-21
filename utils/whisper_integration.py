import whisper

model = whisper.load_model("medium")

def transcribe_audio(audio_file):
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)
    result = model.transcribe(audio)
    print(result['text'])
    return result['text']
