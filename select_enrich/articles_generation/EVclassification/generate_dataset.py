import sys
sys.path.append("../")
sys.path.append("../../")
from utils.embedding_api import embedding_request_ada002
from utils.completion_api import completion_request
import random
import os
import numpy as np

keywords_path = os.path.join("synthetic_data","keywords.txt") 
any_keywords_path = os.path.join("synthetic_data","any_keywords.txt")

keywords = []
with open(keywords_path, 'r') as file:
    keywords = [line.strip() for line in file.readlines()]
any_keywords = []
with open(any_keywords_path, 'r') as file:
    any_keywords = [line.strip() for line in file.readlines()]
    
def select_random_keywords():
    # Ensure there are enough keywords in the list to select from
    if len(keywords) < 3:
        print("Not enough keywords in the file to select from.")
        return []

    # Randomly choose a number of keywords to select, between 3 and 10
    num_keywords_to_choose = random.randint(3, min(10, len(keywords)))

    # Randomly select the chosen number of keywords
    selected_keywords = random.sample(keywords, num_keywords_to_choose)

    return selected_keywords

def select_random_ANY_keywords():
    # Ensure there are enough keywords in the list to select from
    if len(any_keywords) < 3:
        print("Not enough keywords in the file to select from.")
        return []

    # Randomly choose a number of keywords to select, between 3 and 10
    num_keywords_to_choose = random.randint(3, min(10, len(any_keywords)))

    # Randomly select the chosen number of keywords
    selected_keywords = random.sample(any_keywords, num_keywords_to_choose)

    return selected_keywords

def select_random_EV_article():
    i = random.randrange(1,15)
    with open(os.path.join("data","EVcar",f"{i}.txt"), "r") as f:
        return f.read()
        
def select_random_car_article():
    i = random.randrange(1,15)
    with open(os.path.join("data","car",f"{i}.txt"), "r") as f:
        return f.read()
        
def generate_EVnews(folder_path, n_samples = 1000):
    for i in range(n_samples):
        
        prompt= "Generate a news article with html tags inside with the following topics:"+' '.join(select_random_keywords())+"\n please be creative and try to deepen and make some research for enhancement"+\
            "in general or more in detail, whatever you want, also add a bit of noise to these articles"+\
            ("\n you can take some inspiration from "+select_random_EV_article() if random.random() < 0.5 else "")
        article = completion_request(prompt, temperature= 1.8, top_p = 0.8)
        with open(os.path.join(folder_path,"articles",f"{i}.txt"), "w") as f:
            f.write(article)
        embedding = embedding_request_ada002(article)
        np.save(os.path.join(folder_path,"embeddings",f"{i}.npy"),np.array(embedding))


def generate_NonEVNews(folder_path, n_samples = 1000):
    for i in range(n_samples):
        prompt = "Generate a news article with html tags inside about anything you want like:"+ ' '.join(select_random_ANY_keywords()) + "\n but absolutely not EV cars, though you can try to be on the boundary of that "+\
            ("\n you can take some inspiration from "+select_random_car_article() if random.random() < 0.8 else "")
        print(f"Completion request for {i}")
        article = completion_request(prompt, temperature= 1.5, top_p = 0.80)
        with open(os.path.join(folder_path,"articles",f"{i}.txt"), "w") as f:
            f.write(article)
        embedding = embedding_request_ada002(article)
        np.save(os.path.join(folder_path,"embeddings",f"{i}.npy"),np.array(embedding))

if __name__ == "__main__":
    #generate_EVnews(n_samples = 200, folder_path="./synthetic_data/EVcar/")
    generate_NonEVNews(n_samples = 200, folder_path="./synthetic_data/car/")