import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import CharacterCNN
# imports 
# IM LOSING IT 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # chooses either gpu or cpu to use to train model

transform = transforms.Compose([transforms.Resize((28, 28)),
transforms.ToTensor(),
transforms.Normalize((0.5,), (0.5,))]) # makes image into 28 by 28 picture and gives pixel values (tensor)

train_dataset = datasets.EMNIST(# this is to train model on what to figure out the object bigger version of MNIST
    root="./data",              # stores in file named data
    split="balanced",           # makes sure there is no bias of assumption 
    train=True,                 # trains model and downlaods 
    download=True,
    transform=transform) 

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True) # feeds data in small batches to learn

model = CharacterCNN().to(device) # makes the model 
criterion = nn.CrossEntropyLoss() # checks how off model is 
optimizer = optim.Adam(
    model.parameters(), 
    lr=0.0005,
    weight_decay=1e-5
    ) # tries to improve the model
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2) # modulates to learn faster at strt ad slower at end

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
    
    

    print(device)
    print(f"Learning Rate: {current_lr}")
    print(f"Epoch {epoch+1}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.2f}%") # prints the number the model was wrong on 
    
    if epoch_accuracy > best_accuracy: #if the model is better than the last one it saves it
        best_accuracy = epoch_accuracy
        torch.save(model.state_dict(), "best_character_model.pth")
        print("Saved improved model")

print("Model saved successfully.")



