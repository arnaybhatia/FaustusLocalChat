import speech_recognition as sr
import whisper
import numpy as np
import os
import torch

# Define model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models")
MODEL_FILE = os.path.join(MODEL_PATH, "whisper_base.en.pt")

# Create models directory if it doesn't exist
os.makedirs(MODEL_PATH, exist_ok=True)

# Load or download model
try:
    if os.path.exists(MODEL_FILE):
        model = whisper.load_model("base.en")
        model.load_state_dict(torch.load(MODEL_FILE))
        print(f"Loaded model from {MODEL_FILE}")
    else:
        model = whisper.load_model("base.en")
        torch.save(model.state_dict(), MODEL_FILE)
        print(f"Downloaded and saved model to {MODEL_FILE}")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Initialize the recognizer
r = sr.Recognizer()
r.energy_threshold = 1000
r.dynamic_energy_threshold = False
while True:
    # Use the default microphone as the source
    try:
        with sr.Microphone(sample_rate=16000) as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = r.listen(source, timeout=5, phrase_time_limit=None)
    except sr.RequestError as e:
        print(f"Could not access the microphone; {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred while accessing the microphone: {e}")
        exit(1)

    try:
        print("Processing audio...")
        audio_data = audio.get_wav_data()
        data_s16 = np.frombuffer(audio_data, dtype=np.int16, count=len(audio_data)//2, offset=0)
        float_data = data_s16.astype(np.float32, order='C') / 32768.0
        result = model.transcribe(float_data)
        print(result["text"])
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        sleep(.3)