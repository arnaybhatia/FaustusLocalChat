import speech_recognition as sr
import whisper
import numpy as np

model = whisper.load_model("tiny")

# Initialize the recognizer
r = sr.Recognizer()
r.energy_threshold = 4000
r.dynamic_energy_threshold = True

# Use the default microphone as the source
with sr.Microphone(sample_rate=16000) as source:
    print("Say something!")
    audio = r.listen(source, timeout=5, phrase_time_limit=None)
    
try:
    print("Processing audio...")
    audio_data = audio.get_wav_data()
    print(f"Audio data length: {len(audio_data)}")
    
    data_s16 = np.frombuffer(audio_data, dtype=np.int16, count=len(audio_data)//2, offset=0)
    print(f"Converted to np array shape: {data_s16.shape}")
    
    float_data = data_s16.astype(np.float32, order='C') / 32768.0
    print(f"Normalized data range: {float_data.min()} to {float_data.max()}")
    result = model.transcribe(float_data)
    print(result["text"])
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))