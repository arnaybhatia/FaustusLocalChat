from openai import OpenAI
from screen import get_latest_screenshot
import base64
import os
from typing import Optional
import time
from PIL import Image
from dotenv import load_dotenv
import threading
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
    except Exception as e:
        print(f"Image validation error: {e}")
        return False

def get_response(user_input: str, interrupt_event: threading.Event = None) -> str:
    try:
        screenshot_path = get_latest_screenshot()
        print(f"[DEBUG] Got screenshot path: {screenshot_path}")

        system_prompt = """You are a helpful AI assistant. Your responses will be read aloud, so format them to be clear and suitable for text-to-speech output. Focus on being helpful and direct while maintaining a conversational tone. Always organize your responses into clear, structured paragraphs without any bullet points, lists, or line breaks. If you are provided with an image of the screen, only reference it if it is directly relevant to the user's question or request. Otherwise, respond based solely on the user's text input."""

        messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": system_prompt}]

        if screenshot_path and os.path.exists(screenshot_path) and validate_image(screenshot_path):
            base64_image = encode_image(screenshot_path)
            if base64_image:
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{user_input}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                })
            else:
                messages.append({"role": "user", "content": user_input})
        else:
            messages.append({"role": "user", "content": user_input})

        max_retries = 3
        for attempt in range(max_retries):
            try:
                 if interrupt_event and interrupt_event.is_set():
                     return "Response interrupted."

                 response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                 if response.choices and response.choices[0].message and response.choices[0].message.content:
                     return response.choices[0].message.content
                 else:
                    return "No response generated."


            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"[DEBUG] Final API attempt failed: {str(e)}")
                    return "I encountered an error while processing your request. Please try again."
                print(f"[DEBUG] API attempt {attempt + 1} failed, retrying... Error: {e}")
                time.sleep(1)

    except Exception as e:
        print(f"[DEBUG] Error in get_response: {str(e)}")
        return "I encountered an error while processing your request. Please try again."

    return "I encountered an unexpected error. Please try again."
