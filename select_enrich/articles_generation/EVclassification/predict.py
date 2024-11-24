import sys
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from model.SimpleNN import SimpleNN
sys.path.append("../")
sys.path.append("../../")
from utils.embedding_api import embedding_request_ada002
import json
if __name__ == "__main__":
    input_dim = 1536
    model_path = os.path.join('model', 'simple_nn.pth')
    # Example: Load the model (to verify saving works)
    loaded_model = SimpleNN(input_dim)
    loaded_model.load_state_dict(torch.load(model_path))
    loaded_model.eval()
    print("Model successfully loaded and ready for inference.")
    
    
    json_file = "../../../aggregator/output.json"  # Replace with your JSON file path
    with open(json_file, "r", encoding="utf-8") as file:
        json_data = json.load(file)
        article = json_data[7]
        title = article.get("title", "")
        description = article.get("description", "")
        html = article.get("html", "")
        combined_text = title + " " + description + " " + html
        print(f"Generating embedding for article: {title[:10]}...")
        embedding = embedding_request_ada002(combined_text)
        print("prediction:", loaded_model(torch.Tensor(embedding))) #car 0, #EVcar 1