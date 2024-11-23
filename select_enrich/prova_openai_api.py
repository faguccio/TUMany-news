import requests
import json
from utils.util import read_api_key

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
        {"role": "user", "content": "Can you talk to me about what is an electric car?"}
    ],
    "max_tokens": 150,
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
    print("Response:")
    print(response_data["choices"][0]["message"]["content"])
else:
    print(f"Request failed: {response.status_code}")
    print(response.text)
