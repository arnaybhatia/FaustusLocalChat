from openai import OpenAI
from screen import get_latest_screenshot
import base64
import os
from typing import List, Dict, Any, Optional
import time
from PIL import Image

client = OpenAI(
    api_key="not needed",
    base_url="http://localhost:1234/v1"
)

def encode_image(image_path: str) -> Optional[str]:
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return None

def validate_image(image_path: str) -> bool:
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except:
        return False

def get_response(user_input: str) -> str:
    try:
        # Get latest screenshot
        screenshot_path = get_latest_screenshot()
        print(f"[DEBUG] Got screenshot path: {screenshot_path}")

        # Create base messages list with system prompt
        system_prompt = """You are a helpful AI assistant. You aim to provide informative, accurate, and engaging responses while using any available image context to enhance your understanding. Focus on being helpful and direct while maintaining a conversational tone."""

        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt}
        ]

        # Always try to include the screenshot if we have one
        if screenshot_path and os.path.exists(screenshot_path) and validate_image(screenshot_path):
            base64_image = encode_image(screenshot_path)
            if base64_image:
                print(f"[DEBUG] Including screenshot in API call: {screenshot_path}")
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_input},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                })
            else:
                print("[DEBUG] Failed to encode image")
                messages.append({"role": "user", "content": user_input})
        else:
            print("[DEBUG] No valid screenshot available")
            messages.append({"role": "user", "content": user_input})

        # Make API call with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="minicpm-o-2_6",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=8192
                )
                return str(response.choices[0].message.content or "No response generated")
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"[DEBUG] Final API attempt failed: {str(e)}")
                    return "I encountered an error. Please check if LM Studio is running and try again."
                print(f"[DEBUG] API attempt {attempt + 1} failed, retrying... Error: {e}")
                time.sleep(1)

    except Exception as e:
        print(f"[DEBUG] Error in get_response: {str(e)}")
        return "I encountered an error while processing your request. Please try again."

    return "I encountered an unexpected error. Please try again."
