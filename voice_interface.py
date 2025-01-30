from RT_STT import start_listening
from api import get_response
from TTS import TextToSpeech

def start_voice_interface():
    # Voice interface doesn't need screen capture
    start_listening()

if __name__ == "__main__":
    start_voice_interface()
