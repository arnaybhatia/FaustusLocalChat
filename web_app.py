from flask import Flask, render_template, request, jsonify
from api import get_response
import os
import threading

app = Flask(__name__)

# Create directories if they don't exist
for directory in ['./screencaptures', './static']:
    if not os.path.exists(directory):
        os.makedirs(directory)

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

        response = get_response(user_input, None)  # Pass None as interrupt_event

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)
