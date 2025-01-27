from openai import OpenAI
import os

client = OpenAI(
    api_key="not needed",  # LMStudio doesn't need an API key
    base_url="http://localhost:1234/v1"  # Default LMStudio local server URL
)

def get_response(user_input):
    try:
        response = client.chat.completions.create(
            model="meta-llama-3.1-8b-instruct",  # LMStudio uses this model name
            messages=[
                {"role": "system", "content": "You are Faustus, a helpful AI assistant. Keep your responses concise, friendly and natural-sounding since they will be read aloud using text-to-speech. Avoid using special characters, symbols or formatting that may interfere with speech synthesis."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {str(e)}"
