import requests
import json
from utils.util import read_api_key


def embedding_request_ada002(input):
    # Path to the file containing the API key
    api_key_file = "api_key.txt"
    api_key = read_api_key(api_key_file)
    # Azure OpenAI Endpoint and API Key
    endpoint = "https://hackatum-2024.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15"

    # Headers for the HTTP request
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    # Payload for the embedding request
    data = {
        "input": input
    }

    # Sending the POST request
    response = requests.post(endpoint, headers=headers, json=data)

    # Handling the response
    if response.status_code == 200:
        response_data = response.json()
        embeddings = response_data["data"][0]["embedding"]
        return embeddings
    else:
        print(f"Request failed: {response.status_code}")
        print(response.text)
        return None



if __name__ == "__main__":
    embedding = embedding_request_ada002("Prova di embedding")
    if embedding is not None:
        print(embedding)