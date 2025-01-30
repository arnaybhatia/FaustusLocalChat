import speech_recognition as sr
import whisper
import numpy as np
from api import get_response
from TTS import TextToSpeech

def start_listening():
    model = whisper.load_model("base")
    tts = TextToSpeech()

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

        print("\nReady to listen! Say 'Hey John' to start...")
        print("(Press Ctrl+C to stop)")

        try:
            while True:
                try:
                    audio = r.listen(source)
                    audio_data = audio.get_wav_data()
                    data_s16 = np.frombuffer(audio_data, dtype=np.int16, count=len(audio_data)//2, offset=0)
                    float_data = data_s16.astype(np.float32, order='C') / 32768.0

                    result = model.transcribe(float_data)
                    transcribed_text = result["text"].strip()
                    print("\nYou said:", transcribed_text)

                    if "hey john" in transcribed_text.lower():
                        query = transcribed_text.lower().split("hey john", 1)[1].strip()
                        if query:
                            print("\nJohn is thinking...")
                            response = get_response(query)
                            print("John:", response)

                            # Use TTS to speak the response
                            tts.speak(response)

                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"\nError: {str(e)}")
                    continue

        finally:
            # Clean up TTS temporary files when stopping
            tts.cleanup()
            print("\nStopping...")

if __name__ == "__main__":
    start_listening()
