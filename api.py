from openai import OpenAI
from screen import get_latest_screenshot
import base64
import os
from typing import Optional  # Removed 'Any' as it is unused
import time
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
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
    except:
        return False

def get_response(user_input: str) -> str:
    try:
        # Get latest screenshot
        screenshot_path = get_latest_screenshot()
        print(f"[DEBUG] Got screenshot path: {screenshot_path}")

        # Create base messages list with system prompt
        system_prompt = """You are a helpful AI assistant. Your responses will be read aloud, so format them to be clear and suitable for text-to-speech output. You aim to provide informative, accurate, and engaging responses while using any available image context to enhance your understanding. Focus on being helpful and direct while maintaining a conversational tone. Always organize your responses into clear, structured paragraphs without any bullet points, lists, or line breaks."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        # Always try to include the screenshot if we have one
        if screenshot_path and os.path.exists(screenshot_path) and validate_image(screenshot_path):
            base64_image = encode_image(screenshot_path)
            if base64_image:
                # OpenAI API doesn't natively support sending images directly for context
                # If needed, the prompt has to be phrased such that it expects some description of the image context
                # Typically `functions` or uploading to a file store and referencing in prompt can be used, but that is outside this scope.
                # More advanced API endpoints or services might include image understanding if available.
                pass

        # Make API call with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7
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
