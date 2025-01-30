import argparse
from RT_STT import start_listening
from web_app import app, start_background_tasks

def main():
    parser = argparse.ArgumentParser(description='Start Faustus Local Chat')
    parser.add_argument('--mode', choices=['web', 'voice'],
                       default='web', help='Choose interface mode')

    args = parser.parse_args()

    if args.mode == 'web':
        start_background_tasks()  # This starts screen capture
        app.run(debug=True, port=5000)
    elif args.mode == 'voice':
        start_listening()

if __name__ == "__main__":
    main()
