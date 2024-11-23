import requests
import json
from .util import read_api_key

def completion_request(input):
    # Path to the file containing the API key
    api_key_file = "api_key.txt"
    api_key = read_api_key(api_key_file)

    # Azure OpenAI Endpoint and API Key
    endpoint = "https://hackatum-2024.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"


    # Headers for the HTTP request
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    # Payload for the chat completion request
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input}
        ],
        "max_tokens": 6000,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    
    # Sending the POST request
    response = requests.post(endpoint, headers=headers, json=data)

    # Handling the response
    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    else:
        print(f"Request failed: {response.status_code}")
        return None



if __name__ == "__main__":
    response = completion_request("What is an electric car?")
    if response is not None:
        print(response)