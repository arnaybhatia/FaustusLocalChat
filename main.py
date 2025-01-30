import threading
from RT_STT import start_listening
from screen import start_screen_capture

def main():
    # Create and start the screen capture thread
    screen_thread = threading.Thread(target=start_screen_capture, daemon=True)
    screen_thread.start()

    # Start the voice recognition in the main thread
    start_listening()

if __name__ == "__main__":
    main()
