import speech_recognition as sr
import whisper
import numpy as np
import wave
import os
from datetime import datetime
from api import get_response
from TTS import TextToSpeech
import re
import threading
from queue import Queue, Empty
import warnings
import time

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

class VoiceAssistant:
    def __init__(self):
        self.model = whisper.load_model("tiny")
        self.tts = TextToSpeech()
        self.interrupt_event = threading.Event()
        self.audio_queue = Queue()
        self.processing_queue = Queue()
        self.is_speaking = threading.Event()

    def listen_continuously(self, source, recognizer):
        """Thread function to continuously listen for audio"""
        while True:
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=None)
                self.audio_queue.put(audio)
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Listening error: {e}")

    def process_audio_continuously(self):
        """Thread function to process audio and check for triggers"""
        while True:
            try:
                try:
                    audio = self.audio_queue.get(timeout=1)
                except Empty:
                    continue

                print("Processing audio chunk...")
                self.process_single_audio(audio)

            except Exception as e:
                if not isinstance(e, Empty):
                    print(f"Processing error: {str(e)}")
                    import traceback
                    traceback.print_exc()

    def process_single_audio(self, audio):
        try:
            print("Processing audio chunk...")
            audio_data = audio.get_wav_data()
            data_s16 = np.frombuffer(audio_data, dtype=np.int16, count=len(audio_data)//2, offset=0)
            float_data = data_s16.astype(np.float32, order='C') / 32768.0

            print("Running Whisper transcription...")
            result = self.model.transcribe(float_data)

            if not result or "text" not in result:
                print("No transcription result")
                return

            text = result["text"].strip().lower()
            print(f"Transcribed: {text}")

            trigger_pattern = r"(?:hey|hello)\s*john"
            if re.search(trigger_pattern, text):
                print("Trigger phrase detected!")
                if self.is_speaking.is_set():
                    print("Interrupting current speech...")
                    self.interrupt_event.set()
                    self.is_speaking.clear()
                    time.sleep(0.5)  # Give time for cleanup
                    self.interrupt_event.clear()

                query = re.sub(trigger_pattern, "", text).strip()
                if query:
                    self.handle_query(query)
                else:
                    print("No query after trigger phrase")

        except Exception as e:
            print(f"Error in process_single_audio: {e}")
            import traceback
            traceback.print_exc()

    def handle_query(self, query):
        """Handle a single query in a separate thread"""
        try:
            print("\nJohn is thinking...")
            self.is_speaking.set()

            def process_and_speak():
                try:
                    response = get_response(query, self.interrupt_event)
                    if not self.interrupt_event.is_set():
                        print("John:", response)
                        self.tts.speak(response, self.interrupt_event)
                finally:
                    self.is_speaking.clear()

            # Start processing in a new thread
            threading.Thread(target=process_and_speak, daemon=True).start()

        except Exception as e:
            print(f"Error handling query: {e}")
            self.is_speaking.clear()

def start_listening(stt_queue=None):
    try:
        assistant = VoiceAssistant()
        r = sr.Recognizer()
        r.dynamic_energy_threshold = True
        r.pause_threshold = 2.0
        r.phrase_threshold = 0.3
        r.non_speaking_duration = 0.5

        with sr.Microphone(sample_rate=16000) as source:
            print("Calibrating microphone for ambient noise... Please wait...")
            r.adjust_for_ambient_noise(source, duration=5)
            print(f"Initial energy threshold set to: {r.energy_threshold}")

            # Start listening thread
            listen_thread = threading.Thread(
                target=assistant.listen_continuously,
                args=(source, r),
                daemon=True
            )
            listen_thread.start()

            # Start processing thread
            process_thread = threading.Thread(
                target=assistant.process_audio_continuously,
                daemon=True
            )
            process_thread.start()

            print("\nReady to listen! Say 'Hey John' or 'Hello John' to start...")

            # Keep main thread alive and handle keyboard interrupt
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\nStopping...")
                assistant.interrupt_event.set()
                time.sleep(1)  # Give time for threads to clean up

    except Exception as e:
        print(f"Fatal error in speech recognition: {str(e)}")

if __name__ == "__main__":
    start_listening()