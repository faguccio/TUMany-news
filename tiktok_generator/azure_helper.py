import requests
import json
import subprocess
import os
from retry import retry

API_KEY = "2bBZn5pMnk003jcxoOLmZV9lKLflifdjC8mOOSpep0wB9lIaDoAyJQQJ99AKACfhMk5XJ3w3AAABACOGPo7V"

@retry(delay=3, tries=10)
def get_short_phrases(input_json, num_phrases=1):

    with open(input_json, "r") as f:
        data = json.load(f)
    
    input_propt = data[0]["html"]

    input_propt = f"Starting from the following html of a news website, give me {num_phrases} salient regions, each summarized in a max 40 min 30 words phrase for a tiktok, with no numbering:\n{input_propt}"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    # Request body
    data = {
        "messages": [
            {"role": "user", "content": input_propt}
        ],
        "max_tokens": 600
    }

    endpoint = "https://hackatum-2024.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview" 
    response = requests.post(endpoint, headers=headers, json=data)

    # Handle the response
    if response.status_code == 200:
        response_json = response.json()
        phrases = response_json["choices"][0]["message"]["content"].split("\n\n")
        print(f"Generated following phrases:\n{phrases}")
        return phrases
    else:
        raise Exception(f"Request failed: {response.status_code}\n{response.text}")

@retry(delay=3, tries=10)
def generate_prompt(phrase):
    input_propt = f"Starting from the following phrase, give me an image generation prompt for DALL-E, without text for a tiktok:\n{phrase}"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    # Request body
    data = {
        "messages": [
            {"role": "user", "content": input_propt}
        ],
        "max_tokens": 600
    }

    endpoint = "https://hackatum-2024.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview" 
    response = requests.post(endpoint, headers=headers, json=data)

    # Handle the response
    if response.status_code == 200:
        response_json = response.json()
        prompt = response_json["choices"][0]["message"]["content"]
        print(f"Generated following prompt:\n{prompt}")
        return prompt
    else:
        raise Exception(f"Request failed: {response.status_code}\n{response.text}")
    
@retry(delay=3, tries=10)
def generate_single_image(input_propt, output_path):

    # Azure OpenAI Endpoint and API Key
    endpoint = "https://hackatum-2024.openai.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"

    # Headers for the HTTP request
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    # Request body
    data = {
        "prompt": input_propt,
        "n": 1,
        "size": "1024x1792"
    }

    # Sending the POST request
    response = requests.post(endpoint, headers=headers, json=data)

    # Handling the response
    if response.status_code == 200:
        response_data = response.json()
        image_url = response_data["data"][0]["url"]
        image_response = requests.get(image_url)
        with open(output_path, "wb") as f:
            f.write(image_response.content)
    else:
        raise Exception(f"Request failed: {response.status_code}\n{response.text}")


def main():
    # Delete all images from previous runs
    img_folder = "./tmp_images"
    for file_name in os.listdir(img_folder):
        file_path = os.path.join(img_folder, file_name)
        os.remove(file_path)
    

    phrases = get_short_phrases("../aggregator/output.json", 1)

    for phrase in phrases:
        num_prompts = 6
        for i in range(num_prompts):
            prompt = generate_prompt(phrase)

            with open("video.json", "w") as json_file:
                json.dump([{"text": phrase}], json_file, indent=4)

            generate_single_image(prompt, f"tmp_images/image{i}.png") 
            
        args = ["python3", "main.py", "--images=./tmp_images"]
        subprocess.run(args)


if __name__ == "__main__":
    main()
