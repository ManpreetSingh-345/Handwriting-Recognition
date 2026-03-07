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

def rotate_emnist(img):
    return F.rotate(img, -90, fill=0)

def flip_emnist(img):
    return F.hflip(img)

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu") #decides what device to use for training (GPU if available, otherwise CPU)

transform = transforms.Compose([ # Custom pipeline to match EMNIST formatting
    transforms.Grayscale(num_output_channels=1), # Convert to grayscale
    transforms.Lambda(lambda img: F.rotate(img, -90, fill=0)),  # Rotate to match EMNIST orientation
    transforms.Lambda(lambda img: F.hflip(img)), # Flip horizontally to match EMNIST orientation             
    transforms.RandomAffine(degrees=15, translate=(0.1, 0.1), scale=(0.8, 1.2)), # Data augmentation to improve generalization
    transforms.ToTensor(), # Convert to tensor
    transforms.Normalize((0.5,), (0.5,)) # Normalize to match EMNIST's mean and std for better training stability
])

# same pipeline but no augmentation, we want clean images for validation
val_transform = transforms.Compose([ 
    transforms.Grayscale(num_output_channels=1),   # convert to grayscale
    transforms.Lambda(rotate_emnist),              # rotate to match EMNIST orientation
    transforms.Lambda(flip_emnist),                # flip horizontally to match EMNIST orientation
    transforms.ToTensor(),                         # convert to tensor
    transforms.Normalize((0.5,), (0.5,))           # normalize to match training distribution
])

train_dataset = datasets.EMNIST(# this is to train model on what to figure out the object bigger version of MNIST
    root="./data",              # stores in file named data
    split="balanced",           # makes sure there is no bias of assumption 
    train=True,                 # trains model and downlaods 
    download=True,
    transform=transform) 

# separate dataset the model has never seen, used to check if its actually learning
val_dataset = datasets.EMNIST( 
    root="./data",
    split="balanced",
    train=False,         # uses the test split instead of training split
    download=True,
    transform=val_transform) # clean pipeline, no augmentation

if __name__ == '__main__':

    # 256 images per batch, num_workers=0 required on Windows, pin_memory speeds up CPU->GPU transfer
    train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True, num_workers=0, pin_memory=True)  
    # no shuffle for validation so results are consistent
    val_loader = DataLoader(val_dataset, batch_size=256, shuffle=False, num_workers=0, pin_memory=True)

    model = CharacterCNN().to(device) #creates the model and sends it to the device (GPU or CPU)
    criterion = nn.CrossEntropyLoss() #calculates how wrong the model is by comparing its output to the correct answer

    checkpoint_path = "best_character_model.pth"
    if os.path.exists(checkpoint_path):
        print(f"Loading existing weights from {checkpoint_path}...")
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
        
        # Check if it's the NEW dictionary format or the OLD raw weights format
        if isinstance(checkpoint, dict) and "model_state" in checkpoint:
            model.load_state_dict(checkpoint["model_state"]) # load the brain from the hard drive into the model
            best_accuracy = checkpoint["accuracy"]           # load the best accuracy so we dont overwrite a better model
            print(f"Resuming from accuracy: {best_accuracy:.2f}%")
        else:
            # Fallback for old save files
            model.load_state_dict(checkpoint)
            best_accuracy = 0.0
            print("Loaded old format weights! Resetting accuracy tracker to 0.0%")
    else:
        print("No saved model found. Starting from scratch!")
        best_accuracy = 0.0

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

        model.eval() # switches off dropout so we get a clean honest measurement
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad(): # no need to calculate gradients during validation, saves memory
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1) # figures out what the model thinks it is
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()

        val_accuracy = 100 * val_correct / val_total   # figures out validation accuracy
        val_loss = val_loss / len(val_loader)          # figures out validation loss

        scheduler.step(val_loss)                       # modulates learning rate based on validation loss
        current_lr = optimizer.param_groups[0]['lr']   # gets current learning rate
    
        print(f"\nDevice: {device}")
        print(f"Learning Rate: {current_lr}")
        print(f"Epoch {epoch+1}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.2f}%") 
    
        if val_accuracy > best_accuracy: # if the model is better than the last one it saves it
            best_accuracy = val_accuracy
            torch.save({
                "model_state": model.state_dict(), # save the weights
                "accuracy": best_accuracy          # save the accuracy for next run
            }, "best_character_model.pth")
            print("------------------------ Breakthrough! Saved improved model! ------------------------")

    print("\nTraining complete!")   