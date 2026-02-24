import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import torchvision.transforms.functional as F
from torch.utils.data import DataLoader
from model import CharacterCNN
# imports 
# IM LOSING IT 
#Yo chat we lowkey got ts to work

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # chooses either gpu or cpu to use to train model

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Lambda(lambda img: F.rotate(img, -90, fill=0)), # Rotate 90 degrees clockwise
    transforms.Lambda(lambda img: F.hflip(img)),               # Flip horizontally
    transforms.ToTensor(),
])

train_dataset = datasets.EMNIST(# this is to train model on what to figure out the object bigger version of MNIST
    root="./data",              # stores in file named data
    split="balanced",           # makes sure there is no bias of assumption 
    train=True,                 # trains model and downlaods 
    download=True,
    transform=transform) 
print(train_dataset.classes)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True) # feeds data in small batches to learn

model = CharacterCNN().to(device) # makes the model 
criterion = nn.CrossEntropyLoss() # checks how off model is 
optimizer = optim.Adam(model.parameters(), lr=0.001) # tries to improve the model

# This part i believe should fix the saving problem
checkpoint_path = "character_model.pth" # this makes the path to the save file
if os.path.exists(checkpoint_path): # this checks if it exists 
    model.load_state_dict(torch.load(checkpoint_path, map_location=device)) # this loads the original state it was in from the last run
    print("Previous weights found! Resuming training...")
else:
    print("No saved model found. Starting from scratch!")

epochs = 5 #makes the model go through dataset 5 times

for epoch in range(epochs):
    running_loss = 0.0 # starts loss count from 0

    for images, labels in train_loader: #takes 64 images per batch 
        images, labels = images.to(device), labels.to(device) #decides what device to use 

        optimizer.zero_grad() #clears the old errosr
        outputs = model(images) #sends images through 
        loss = criterion(outputs, labels) # checks answers 
        loss.backward() #weighs the how wrong it was 
        optimizer.step() #changes paramater to get right next time 
        running_loss += loss.item() #adds error loss weight and sees total

    print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader):.4f}") # prints the number the model was wrong on 
    torch.save(model.state_dict(), "character_model.pth")#saves learnt weight for future reference 
print("Model saved successfully.")

#wanted to see if this works

