import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from model.SimpleNN import SimpleNN
if __name__ == "__main__":
    # Paths to the embedding folders
    car_embeddings_path = os.path.join('synthetic_data', 'car', 'embeddings')
    evcar_embeddings_path = os.path.join('synthetic_data','EVcar','embeddings')

    # Function to load embeddings and assign labels
    def load_embeddings_and_labels(path, label):
        embeddings = []
        for file in os.listdir(path):
            if file.endswith('.npy'):
                filepath = os.path.join(path, file)
                embedding = np.load(filepath)
                embeddings.append((embedding, label))
        return embeddings
    
    # Load car (label=0) and EVcar (label=1) embeddings
    car_data = load_embeddings_and_labels(car_embeddings_path, 0)
    evcar_data = load_embeddings_and_labels(evcar_embeddings_path, 1)
    print(len(car_data))
    # Combine and prepare the dataset
    data = car_data + evcar_data
    X, y = zip(*data)  # X: features, y: labels
    X = np.array(X, dtype=np.float32)  # Ensure embeddings are floats
    y = np.array(y, dtype=np.float32)  # Labels as floats for PyTorch

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Convert data to PyTorch tensors
    X_train_tensor = torch.tensor(X_train)
    y_train_tensor = torch.tensor(y_train).unsqueeze(1)  # Add dimension for binary classification
    X_test_tensor = torch.tensor(X_test)
    y_test_tensor = torch.tensor(y_test).unsqueeze(1)

    # Initialize the model
    input_dim = X_train.shape[1]  # Number of features in embeddings
    model = SimpleNN(input_dim)

    # Define loss function and optimizer
    criterion = nn.BCELoss()  # Binary Cross-Entropy Loss
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    epochs = 80
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()

        # Forward pass
        outputs = model(X_train_tensor)
        loss = criterion(outputs, y_train_tensor)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        # Print loss for every 10th epoch
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")

    # Evaluation
    model.eval()
    with torch.no_grad():
        y_pred = model(X_test_tensor)
        y_pred_classes = (y_pred > 0.5).float()  # Convert probabilities to binary predictions

    # Calculate accuracy
    accuracy = accuracy_score(y_test_tensor, y_pred_classes)
    print("Accuracy:", accuracy)

    # Classification report
    print("Classification Report:\n", classification_report(y_test_tensor, y_pred_classes))
    
    # Save the trained model
    model_path = os.path.join('model', 'simple_nn.pth')  # Path to save the model
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")

    # Example: Load the model (to verify saving works)
    loaded_model = SimpleNN(input_dim)
    loaded_model.load_state_dict(torch.load(model_path))
    loaded_model.eval()
    print("Model successfully loaded and ready for inference.")
    print("Input dim", input_dim)

