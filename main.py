import argparse
from RT_STT import start_listening
from web_app import app
import threading
from screen import start_screen_capture


_screen_thread = None  # Global variable to hold the screen capture thread


def start_screen_thread():
    global _screen_thread
    if _screen_thread is None or not _screen_thread.is_alive():
        _screen_thread = threading.Thread(target=start_screen_capture, daemon=True)
        _screen_thread.start()
    return _screen_thread


def main():
    parser = argparse.ArgumentParser(description='Start Faustus Local Chat')
    parser.add_argument(
        '--mode',
        choices=['web', 'voice'],
        default='web',
        help='Choose interface mode'
    )

    args = parser.parse_args()

    # Start screen capture for both modes
    start_screen_thread()

    if args.mode == 'web':
        app.run(debug=True, port=5000)
    elif args.mode == 'voice':
        start_listening()


if __name__ == "__main__":
    main()
