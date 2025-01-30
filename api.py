from openai import OpenAI
from screen import get_latest_screenshot
import base64
import os
from typing import List, Dict, Any

client = OpenAI(
    api_key="not needed",
    base_url="http://localhost:1234/v1"
)

def get_response(user_input: str) -> str:
    try:
        screenshot_path = get_latest_screenshot()

        if "hey john" in user_input.lower():
            user_input = user_input.lower().split("hey john", 1)[1].strip()

        messages: List[Dict[str, Any]] = [
            {
                "role": "system",
                "content": "You are John, a helpful AI assistant. Keep your responses concise, friendly and natural-sounding."
            }
        ]

        if screenshot_path and os.path.exists(screenshot_path):
            try:
                with open(screenshot_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_input
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                })
            except Exception as e:
                print(f"Error processing image: {str(e)}")
                messages.append({
                    "role": "user",
                    "content": user_input
                })
        else:
            messages.append({
                "role": "user",
                "content": user_input
            })

        response = client.chat.completions.create(
            model="minicpm-o-2_6",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        return "I encountered an error while processing your request. Please try again."
