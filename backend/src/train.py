import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import CharacterCNN
# imports 
# IM LOSING IT 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # chooses either gpu or cpu to use to train model

transform = transforms.Compose([transforms.Resize((28, 28)),transforms.ToTensor(),]) # makes image into 28 by 28 picture and gives pixel values (tensor)

train_dataset = datasets.EMNIST(# this is to train model on what to figure out the object bigger version of MNIST
    root="./data",              # stores in file named data
    split="balanced",           # makes sure there is no bias of assumption 
    train=True,                 # trains model and downlaods 
    download=True,
    transform=transform) 

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True) # feeds data in small batches to learn

model = CharacterCNN().to(device) # makes the model 
criterion = nn.CrossEntropyLoss() # checks how off model is 
optimizer = optim.Adam(model.parameters(), lr=0.001) # tries to improve the model

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

