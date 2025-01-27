# Faustus Local Chat

A real-time speech-to-text application that uses Whisper for transcription and LMStudio for local LLM interactions. The application listens for voice input and responds when addressed as "Faustus".

## Features

- Real-time speech recognition using OpenAI's Whisper model
- Local LLM integration via LMStudio
- Continuous listening and response capability
- Low latency voice transcription
- No cloud API dependencies

## Prerequisites

- Python 3.10 or higher
- LMStudio running locally on port 1234
- Working microphone

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd FaustusLocalChat
```

2. Install required packages:
```bash
pip install openai-python
pip install whisper
pip install speechrecognition
pip install numpy
```

3. Ensure LMStudio is running locally with the following settings:
   - Server running on port 1234
   - Model loaded (preferably Meta-Llama2)

## Usage

1. Start LMStudio and ensure the local server is running

2. Run the application:
```bash
python RT_STT.py
```

3. Speak to Faustus:
   - The application will continuously listen for speech
   - Say "Faustus" followed by your question/command
   - Wait for the response

4. To exit, press Ctrl+C

## Project Structure

- `RT_STT.py` - Main application file handling speech recognition and transcription
- `api.py` - LLM integration with LMStudio
- `.gitignore` - Git ignore file
- `README.md` - Project documentation

## Configuration

The application uses default settings that should work for most setups:
- Speech recognition energy threshold: 300
- Dynamic energy threshold: Enabled
- Pause threshold: 1.0 seconds
- Phrase threshold: 0.3 seconds

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```

This README.md provides:
- Clear project description
- Installation instructions
- Usage guide
- Project structure
- Configuration details
- Contributing guidelines
- License information

You may want to customize:
- The repository URL
- Specific version requirements
- Any additional setup steps specific to your environment
- License type if different from MIT
