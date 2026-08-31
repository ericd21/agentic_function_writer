import requests

# LLM Configuration (local lightweight inference)
API_URL = "http://localhost:8080/v1/chat/completions"
MODEL = "mistral-7b-instruct-v0.1.Q4_K_M"

MAX_TOKENS = 4096 if MODEL == "mistral-7b-instruct-v0.1.Q4_K_M" else 8192

# LLM Call
def call_llm(messages: list[dict[str,str]], temperature: float = 0.2) -> str:
     """
    LLM Adapter
    Sends messages to the local inference server and returns the assistant's text.
    """
     
    payload = {
        "model": MODEL, 
        "messages": messages, 
        "temperature": temperature
    }

    response = requests.post(API_URL, json=payload, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(f"LLM server error: {response.status_code} - {response.text}")

    try:
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        raise RuntimeError(f"Malformed LLM response: {response.text}") from e