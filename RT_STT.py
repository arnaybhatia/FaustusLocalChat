import speech_recognition as sr
import whisper
import numpy as np
import time
from api import get_response

model = whisper.load_model("base")

# Initialize the recognizer
r = sr.Recognizer()
r.energy_threshold = 300
r.dynamic_energy_threshold = True
r.pause_threshold = 1.0
r.phrase_threshold = 0.3

# Use the default microphone as the source
with sr.Microphone(sample_rate=16000) as source:
    print("Adjusting for ambient noise... Please wait...")
    r.adjust_for_ambient_noise(source, duration=2)
    print(f"Energy threshold set to: {r.energy_threshold}")

    print("\nReady to listen! Speak now...")
    print("(Press Ctrl+C to stop)")

    while True:
        try:
            audio = r.listen(source,
                           timeout=None,  # No timeout
                           phrase_time_limit=None)  # No phrase time limit

            audio_data = audio.get_wav_data()
            data_s16 = np.frombuffer(audio_data, dtype=np.int16, count=len(audio_data)//2, offset=0)
            float_data = data_s16.astype(np.float32, order='C') / 32768.0

            result = model.transcribe(float_data)
            transcribed_text = result["text"].strip()
            print("\nYou said:", transcribed_text)

            # Check if the transcribed text contains "Faustus"
            if "faustus" in transcribed_text.lower():
                print("\nFaustus is thinking...")
                response = get_response(transcribed_text)
                print("Faustus:", response)

        except KeyboardInterrupt:
            print("\nStopping...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            continue
