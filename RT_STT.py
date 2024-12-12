import whisper

model = whisper.load_model("turbo")
result = model.transcribe("tiny.mp3")
print(result["text"])