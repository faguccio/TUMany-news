import sys
sys.path.append("../")
sys.path.append("../../")
from utils.embedding_api import embedding_request_ada002
import os
import numpy as np

def generate_embedding_car():
    # Path to the 'car' folder
    car_folder = os.path.join('data', 'car')

    # Iterate through the files in the 'car' folder
    if os.path.exists(car_folder):
        for filename in os.listdir(car_folder):
            # Check if the file is a .txt file
            if filename.endswith('.txt'):
                file_path = os.path.join(car_folder, filename)
                
                # Open and process the .txt file
                with open(file_path, 'r') as file:
                    content = file.read()
                    embedding = embedding_request_ada002(content)
                    np.save(os.path.join("data","embedding","car",filename.split(".")[0]),embedding) 
                    #print(f"Contents of {filename}:\n{content}\n")
    else:
        print(f"The folder '{car_folder}' does not exist.")
def generate_embedding_evcar():
    # Path to the 'car' folder
    car_folder = os.path.join('data', 'EVcar')

    # Iterate through the files in the 'car' folder
    if os.path.exists(car_folder):
        for filename in os.listdir(car_folder):
            # Check if the file is a .txt file
            if filename.endswith('.txt'):
                file_path = os.path.join(car_folder, filename)
                
                # Open and process the .txt file
                with open(file_path, 'r') as file:
                    content = file.read()
                    embedding = embedding_request_ada002(content)
                    np.save(os.path.join("data","embedding","EVcar",filename.split(".")[0]),embedding) 
                    #print(f"Contents of {filename}:\n{content}\n")
    else:
        print(f"The folder '{car_folder}' does not exist.")


if __name__ == "__main__":
    generate_embedding_car()
    generate_embedding_evcar()

    
