import speech_recognition as sr
import whisper
import numpy as np
from api import get_response
from TTS import TextToSpeech

def start_listening(stt_queue=None):
    try:
        model = whisper.load_model("turbo")
        tts = TextToSpeech()

        # Initialize the recognizer with more lenient settings
        r = sr.Recognizer()
        r.energy_threshold = 150  # Lower threshold for better sensitivity
        r.dynamic_energy_threshold = True
        r.pause_threshold = 2.0  # Shorter pause threshold
        r.phrase_threshold = 0.3
        r.non_speaking_duration = 1.0  # Shorter duration for non-speaking

        # Use the default microphone as the source
        with sr.Microphone(sample_rate=16000) as source:
            print("Adjusting for ambient noise... Please wait...")
            # Longer ambient noise adjustment
            r.adjust_for_ambient_noise(source, duration=5)
            print(f"Energy threshold set to: {r.energy_threshold}")

            print("\nReady to listen! Say 'Hey John' to start...")
            print("(Press Ctrl+C to stop)")

            try:
                while True:
                    try:
                        # Use listen_in_background for continuous listening
                        audio = r.listen(source, timeout=None, phrase_time_limit=None)
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

                                # Put query in queue if provided
                                if stt_queue is not None:
                                    stt_queue.put(query)

                                # Use TTS to speak the response
                                tts.speak(response)

                    except KeyboardInterrupt:
                        raise
                    except Exception as e:
                        print(f"\nError in speech recognition: {str(e)}")
                        continue

            finally:
                # Clean up TTS temporary files when stopping
                tts.cleanup()
                print("\nStopping...")

    except Exception as e:
        print(f"Fatal error in speech recognition: {str(e)}")

if __name__ == "__main__":
    start_listening()
