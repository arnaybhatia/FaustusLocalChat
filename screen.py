import pyautogui
import time
import os
from datetime import datetime
from PIL import Image
from io import BytesIO

def validate_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception as e:
        print(f"Image validation error: {e}")
        return False

def cleanup_old_screenshots(screenshot_dir, max_files=2):  # Reduced max files
    try:
        files = sorted([os.path.join(screenshot_dir, f) for f in os.listdir(screenshot_dir)
                       if f.startswith("screenshot_") and f.endswith(".png")],
                      key=os.path.getctime)
        while len(files) > max_files:
            try:
                os.remove(files[0])
                files.pop(0)
            except Exception as e:
                print(f"Error removing file: {e}")
                break
    except Exception as e:
        print(f"Error cleaning up screenshots: {e}")

def get_latest_screenshot():
    screenshot_dir = "./screencaptures"
    if not os.path.exists(screenshot_dir):
        print("Screenshot directory does not exist")
        return None

    try:
        files = [f for f in os.listdir(screenshot_dir)
                if f.startswith("screenshot_") and f.endswith(".png")]
        if not files:
            print("No screenshot files found")
            return None

        latest_file = max([os.path.join(screenshot_dir, f) for f in files],
                         key=os.path.getctime)

        # Check if file is too old (> 2 seconds)
        age = time.time() - os.path.getctime(latest_file)
        print(f"Latest screenshot age: {age:.2f} seconds")
        if age > 2:  # Reduced from 5 to 2 seconds
            print("Screenshot too old")
            return None

        if validate_image(latest_file):
            print(f"Using screenshot: {latest_file}")
            return latest_file
        return None
    except Exception as e:
        print(f"Error getting latest screenshot: {e}")
        return None

def start_screen_capture():
    screenshot_dir = "./screencaptures"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
        print(f"Created screenshot directory: {screenshot_dir}")

    last_capture_time = 0
    min_interval = 0.2  # Reduced from 0.5 to 0.2 seconds

    while True:
        try:
            current_time = time.time()
            if current_time - last_capture_time < min_interval:
                time.sleep(0.05)  # Reduced sleep time
                continue

            print(f"Taking screenshot at {datetime.now()}")
            screenshot = pyautogui.screenshot()

            img = screenshot.resize((800, 600), Image.Resampling.LANCZOS)

            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG', optimize=True, quality=85)

            img_byte_arr.seek(0)
            test_image = Image.open(img_byte_arr)
            test_image.verify()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
            img_byte_arr.seek(0)
            with open(filepath, 'wb') as f:
                f.write(img_byte_arr.getvalue())

            print(f"Saved screenshot: {filepath}")
            cleanup_old_screenshots(screenshot_dir)
            last_capture_time = time.time()

        except Exception as e:
            print(f"Error capturing screen: {str(e)}")
            time.sleep(0.5)  # Reduced error retry time
            continue
