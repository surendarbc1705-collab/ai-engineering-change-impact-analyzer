import ollama
import json


def ask_ai(prompt: str):

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    return json.loads(response["message"]["content"])