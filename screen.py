import pyautogui
import time
import os
from datetime import datetime
from PIL import Image
import numpy as np

def get_latest_screenshot():
    screenshot_dir = "./screencaptures"
    if not os.path.exists(screenshot_dir):
        return None

    files = os.listdir(screenshot_dir)
    if not files:
        return None

    latest_file = max([os.path.join(screenshot_dir, f) for f in files], key=os.path.getctime)
    return latest_file

def start_screen_capture():
    screenshot_dir = "./screencaptures"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    while True:
        try:
            # Take screenshot and convert to numpy array
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)

            # Convert numpy array back to PIL Image
            img = Image.fromarray(screenshot_np)

            # Resize
            width = 800
            height = 600
            img = img.resize((width, height), Image.Resampling.LANCZOS)

            # Save with a unique filename
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(screenshot_dir, f"screenshot_{current_time}.png")
            img.save(filepath, format='PNG', optimize=True)

            time.sleep(0.2)  # Reduced frequency of captures

        except Exception as e:
            print(f"Error capturing screen: {str(e)}")
            time.sleep(0.1)
            continue
