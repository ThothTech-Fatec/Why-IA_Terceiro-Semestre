import os
from pydub import AudioSegment


def convert_to_wav(input_file, output_file="converted_audio.wav"):
    """Convert audio file to WAV format with a specified output file name."""
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"The file {input_file} does not exist.")
    
    try:
      
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format="wav")
        print(f"File successfully converted to {output_file}.")
        return output_file
    except Exception as e:
        print(f"Error converting file: {e}")
        raise

def clean_up(files):
    """Remove temporary files and handle exceptions."""
    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"Removed {file}.")
            else:
                print(f"{file} does not exist.")
        except Exception as e:
            print(f"Error removing {file}: {e}")
