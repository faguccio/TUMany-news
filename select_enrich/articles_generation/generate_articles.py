import sys
sys.path.append("../")
import time
from utils.embedding_api import embedding_request_ada002
from utils.completion_api import completion_request
from utils.util import read_api_key
import os
import json
import requests
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import silhouette_score



import plotly.express as px
import pandas as pd

from sklearn.manifold import TSNE
import umap.umap_ as umap


# Process JSON input to extract embeddings
def process_json(json_data):
    embeddings = []
    labels = []
    for article in json_data:
        title = article.get("title", "")
        description = article.get("description", "")
        html = article.get("html", "")
        combined_text = title + " " + description + " " + html
        print(f"Generating embedding for article: {title[:10]}...")
        embedding = embedding_request_ada002(combined_text)
        if embedding is not None:
            embeddings.append(embedding)
            labels.append(title)  # Use the title as a label
    return np.array(embeddings), labels

# Dimensionality reduction using t-SNE or UMAP
def perform_dimensionality_reduction(embeddings, method="umap", n_components=3):
    print(f"Performing dimensionality reduction using {method.upper()}...")
    if method == "tsne":
        reducer = TSNE(n_components=n_components, random_state=42, perplexity=10, n_iter=1000)
    elif method == "umap":
        reducer = umap.UMAP(n_components=n_components, random_state=42, n_neighbors=15, min_dist=0.1)
    else:
        raise ValueError("Unsupported dimensionality reduction method. Use 'tsne' or 'umap'.")
    reduced_embeddings = reducer.fit_transform(embeddings)
    return reduced_embeddings
# Perform clustering
def perform_clustering(embeddings, n_clusters):
    print(f"Performing KMeans clustering with {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(embeddings)
    return cluster_labels

# Automatically choose the number of clusters using silhouette score
def choose_optimal_clusters(embeddings, max_clusters=10):
    print("Finding optimal number of clusters...")
    best_score = -1
    best_k = 2  # Minimum number of clusters
    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        cluster_labels = kmeans.fit_predict(embeddings)
        score = silhouette_score(embeddings, cluster_labels)
        print(f"Silhouette score for {k} clusters: {score:.4f}")
        if score > best_score:
            best_score = score
            best_k = k
    print(f"Optimal number of clusters: {best_k}")
    return best_k

def visualize_embeddings_3d(embeddings, labels, clusters=None):
    print("Visualizing embeddings interactively in 3D...")
    # Convert embeddings and metadata into a DataFrame
    data = pd.DataFrame(embeddings, columns=["PC1", "PC2", "PC3"])
    data["Label"] = [s[:10] for s in labels] 
    if clusters is not None:
        data["Cluster"] = clusters
    else:
        data["Cluster"] = "None"
    
    # Create the 3D scatter plot
    fig = px.scatter_3d(
        data,
        x="PC1",
        y="PC2",
        z="PC3",
        color="Cluster",
        text="Label",
        title="Interactive 3D Embedding Visualization",
        labels={"Cluster": "Cluster ID"}
    )
    fig.update_traces(marker=dict(size=5, opacity=0.8))
    fig.show()
    
def generate_article_from_cluster(cluster_labels, labels, descriptions, htmls, output_folder="output_articles"):
    """
    This function generates an article from each cluster and saves it as a .txt file, including HTML content.
    
    Args:
        cluster_labels (list): The cluster labels for each article.
        labels (list): The list of article titles.
        descriptions (list): The list of article descriptions.
        htmls (list): The list of HTML content for each article.
        output_folder (str): The folder where generated articles will be saved. Default is "cluster_articles".
    
    Returns:
        None
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate over each cluster
    for cluster_id in set(cluster_labels):
        # Collect the titles, descriptions, and HTMLs of articles in the current cluster
        cluster_text = []
        for i, cluster in enumerate(cluster_labels):
            if cluster == cluster_id:
                article_text = f"Title: {labels[i]}\nDescription: {descriptions[i]}\n\nHTML Content:\n{htmls[i]}\n\n"
                cluster_text.append(article_text)
        
        cluster_article = generate_big_article_from_cluster(cluster_text)
        
        # Save the generated article to a text file
        output_file = os.path.join(output_folder, f"cluster_{cluster_id}.json")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(cluster_article, file)
        
        print(f"Article for Cluster {cluster_id} saved to {output_file}")

def generate_big_article_from_cluster(cluster_text):
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
    #Summarize articles to create context
    messages = [{"role": "system", "content": "You are a helpful assistant providing news articles."}]
    for article in cluster_text:
        messages.append(
                {
                    "role": "user",
                    "content": "Summarize the following article:\n" + article 
                }
            )
        # Payload for the chat completion request
        data = {
            "messages": messages,
            "max_tokens": 8000,
            "temperature": 0.7,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        # Sending the POST request
        response = requests.post(endpoint, headers=headers, json=data)
        status_code = response.status_code
        while status_code != 200:
            time.sleep(10)
            response = requests.post(endpoint, headers=headers, json=data)
            status_code = response.status_code
            
        response = response.json()
        response = response["choices"][0]["message"]["content"]
        messages.append(
                {
                    "role": "system",
                    "content": response 
                }
            )
    #Get structure of article
    messages.append(
                {
                    "role": "user",
                    "content": "Great, now could you please generate the structure of a novel article based from the context that I gave you?"+\
                        "Your output must be a json dictionary with the following format:\n"+\
                        "{\"title\": \"<INSERT TITLE OF NEWS ARTICLE>\", \"sections\": [{\"title\":\"<INSERT SECTION TITLE>\"},{...},...]}" 
                }
            )
    response = requests.post(endpoint, headers=headers, json=data)
    status_code = response.status_code
    while status_code != 200:
        time.sleep(10)
        response = requests.post(endpoint, headers=headers, json=data)
        status_code = response.status_code
        
    response = response.json()
    response = response["choices"][0]["message"]["content"]
    messages.append(
            {
                "role": "system",
                "content": response 
            }
        )
    response = response.replace("```json","").replace("```", "")
    print(response)
    final_sections = []
    
    article_structure = dict(json.loads(response))
    sections_structure = article_structure["sections"]
    
    for section in sections_structure:
        section_title = section["title"]
        messages.append(
                {
                    "role": "user",
                    "content": f"Given the whole context of the articles I gave you, generate the content for the section \"{section_title}\" providing insightful opinions and making a very SEO optimized news article. Provide only plain text, no titles or other sections." 
                }
            )
        response = requests.post(endpoint, headers=headers, json=data)
        status_code = response.status_code
        while status_code != 200:
            time.sleep(10)
            response = requests.post(endpoint, headers=headers, json=data)
            status_code = response.status_code
            
        response = response.json()
        response = response["choices"][0]["message"]["content"]
                    
        messages.append(
                {
                    "role": "system",
                    "content": response 
                }
            )
        final_sections.append({"title":section_title,"content":response})
    article_structure["sections"] = final_sections
    return article_structure
    
    


    

if __name__ == "__main__":
    # Example JSON input (replace this with reading from a file or API)
    json_file = "../../aggregator/output.json"  # Replace with your JSON file path
    with open(json_file, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    embeddings, labels = process_json(json_data)

    # Automatically determine the number of clusters
    max_clusters = 10  # Set a reasonable upper limit for clusters
    optimal_clusters = choose_optimal_clusters(embeddings, max_clusters)

    # Perform clustering on raw embeddings
    cluster_labels = perform_clustering(embeddings, optimal_clusters)

    # Extract article descriptions and HTML content
    descriptions = [article.get("description", "") for article in json_data]
    htmls = [article.get("html", "") for article in json_data]

    # Generate articles from clusters and save to files
    generate_article_from_cluster(cluster_labels, labels, descriptions, htmls)
    