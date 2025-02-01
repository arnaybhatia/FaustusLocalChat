# Faustus Local Chat

A versatile chat assistant with both voice and web interfaces that can run completely locally or leverage OpenAI's GPT-4V for enhanced capabilities. The voice interface uses Whisper for transcription and responds when addressed as "John".

## Features

- Real-time speech recognition using OpenAI's Whisper model
- Choice between local LLM or OpenAI GPT-4V integration  
- Web interface with real-time screen context
- Voice interface with continuous listening
- Low latency voice transcription
- Screen capture and analysis capabilities

## Prerequisites

- Python 3.10 or higher
- Working microphone (for voice interface)
- OpenAI API key (optional)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd FaustusLocalChat
```

2. Create and activate conda environment:
```bash
conda env create -f environment.yml
conda activate faustus
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up OpenAI API key (optional):
Create a .env file with:
```
OPENAI_API_KEY=your_key_here
```

## Usage

1. Start the web interface:
```bash
python main.py --mode web
```

2. Start the voice interface:
```bash
python main.py --mode voice
```

3. Using voice interface:
   - The application will continuously listen for speech
   - Say "Hey John" or "Hello John" followed by your question
   - Wait for the response

4. To exit, press Ctrl+C

## Project Structure

- `main.py` - Main application entry point
- `RT_STT.py` - Voice interface and speech recognition
- `web_app.py` - Flask web interface
- `api.py` - LLM integration (local or OpenAI)
- `screen.py` - Screen capture functionality
- `TTS.py` - Text-to-speech engine

## Configuration

Voice interface settings:
- Dynamic energy threshold: Enabled
- Pause threshold: 2.0 seconds
- Phrase threshold: 0.3 seconds
- Non-speaking duration: 0.5 seconds

Screen capture settings:
- Resolution: 800x600
- Capture interval: 0.2 seconds
- PNG compression quality: 85

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
