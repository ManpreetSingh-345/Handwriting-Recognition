import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import torchvision.transforms.functional as F
from torch.utils.data import DataLoader
from model import CharacterCNN
#imports
#im LOSING IT
#im going to crack this code >:D

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #decides what device to use for training (GPU if available, otherwise CPU)

transform = transforms.Compose([ # Custom pipeline to match EMNIST formatting
    transforms.Grayscale(num_output_channels=1), # Convert to grayscale
    transforms.Lambda(lambda img: F.rotate(img, -90, fill=0)),  # Rotate to match EMNIST orientation
    transforms.Lambda(lambda img: F.hflip(img)), # Flip horizontally to match EMNIST orientation             
    transforms.RandomAffine(degrees=15, translate=(0.1, 0.1), scale=(0.8, 1.2)), # Data augmentation to improve generalization
    transforms.ToTensor(), # Convert to tensor
    transforms.Normalize((0.5,), (0.5,)) # Normalize to match EMNIST's mean and std for better training stability
])

train_dataset = datasets.EMNIST(# this is to train model on what to figure out the object bigger version of MNIST
    root="./data",              # stores in file named data
    split="balanced",           # makes sure there is no bias of assumption 
    train=True,                 # trains model and downlaods 
    download=True,
    transform=transform) 

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True) #64 images per batch, shuffles data for better training

model = CharacterCNN().to(device) #creates the model and sends it to the device (GPU or CPU)
criterion = nn.CrossEntropyLoss() #calculates how wrong the model is by comparing its output to the correct answer

checkpoint_path = "best_character_model.pth"
if os.path.exists(checkpoint_path):
    print(f"Loading existing weights from {checkpoint_path}...")
    # Load the brain from the hard drive into the model
    model.load_state_dict(torch.load(checkpoint_path, weights_only=True))
else:
    print("No saved model found. Starting from scratch!")

optimizer = optim.Adam(model.parameters(), lr=0.0005, weight_decay=1e-5) # L2 regularization to prevent overfitting
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)# Reduce learning rate if validation loss doesn't improve for 2 epochs

epochs = 5 #makes the model go through dataset 5 times
best_accuracy = 0.0 # starts accuracy count from 0


for epoch in range(epochs):
    model.train() #tells model to train
    running_loss = 0.0 # starts loss count from 0
    correct = 0 # starts correct count from 0
    total = 0 # starts total count from 0

    for images, labels in train_loader: #takes 64 images per batch 
        images, labels = images.to(device), labels.to(device) #decides what device to use 

        optimizer.zero_grad() #clears the old errosr
        outputs = model(images) #sends images through 
        loss = criterion(outputs, labels) # checks answers 
        loss.backward() #weighs the how wrong it was 
        optimizer.step() #changes paramater to get right next time 
        running_loss += loss.item() #adds error loss weight and sees total
        _, predicted = torch.max(outputs.data, 1) #figures out what the model thinks it is
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
    epoch_accuracy = 100 * correct / total #figures out accuracy of model
    epoch_loss = running_loss / len(train_loader) #figures out loss of model 
    scheduler.step(epoch_loss) #modulates learning rate
    current_lr = scheduler.get_last_lr()[0] # gets current learning rate
    
    print(f"\nDevice: {device}")
    print(f"Learning Rate: {current_lr}")
    print(f"Epoch {epoch+1}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.2f}%") 
    
    if epoch_accuracy > best_accuracy: #if the model is better than the last one it saves it
        best_accuracy = epoch_accuracy
        torch.save(model.state_dict(), "best_character_model.pth")
        print("  -> Saved improved model!")

print("\nTraining complete!")   