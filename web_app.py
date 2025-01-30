from flask import Flask, render_template, request, jsonify
from api import get_response
import os
from screen import start_screen_capture
import threading

app = Flask(__name__)

# Create directories if they don't exist
for directory in ['./screencaptures', './static']:
    if not os.path.exists(directory):
        os.makedirs(directory)

_screen_thread = None

def start_background_tasks():
    global _screen_thread
    if _screen_thread is None or not _screen_thread.is_alive():
        _screen_thread = threading.Thread(target=start_screen_capture, daemon=True)
        _screen_thread.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        if not request.json:
            return jsonify({'error': 'No JSON data received'}), 400

        user_input = request.json.get('message', '')

        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        response = get_response(user_input)

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    start_background_tasks()
    app.run(debug=False, port=5000)
