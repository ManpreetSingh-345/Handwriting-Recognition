import os
import torch
import torch.nn as nn
import torch.optim as optim
import multiprocessing
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import CharacterCNN
#imports
#im LOSING IT
#im going to crack this code >:D

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # decides what device to use for training (GPU if available, otherwise CPU)

transform = transforms.Compose([ # custom pipeline to match EMNIST formatting, includes augmentation to improve generalization
    transforms.Grayscale(num_output_channels=1),                                  # convert to grayscale
    transforms.RandomRotation(degrees=(-90, -90)),                                # rotate to match EMNIST orientation
    transforms.RandomHorizontalFlip(p=1.0),                                       # flip horizontally to match EMNIST orientation
    transforms.RandomAffine(degrees=15, translate=(0.1, 0.1), scale=(0.8, 1.2)), # randomly distorts image so model doesnt memorize exact images
    transforms.ToTensor(),                                                         # convert to tensor
    transforms.Normalize((0.5,), (0.5,))                                          # normalize to match EMNIST's mean and std for better training stability
])

val_transform = transforms.Compose([ # same pipeline but no augmentation, we want clean images for validation
    transforms.Grayscale(num_output_channels=1),   # convert to grayscale
    transforms.RandomRotation(degrees=(-90, -90)), # rotate to match EMNIST orientation
    transforms.RandomHorizontalFlip(p=1.0),        # flip horizontally to match EMNIST orientation
    transforms.ToTensor(),                          # convert to tensor
    transforms.Normalize((0.5,), (0.5,))           # normalize to match training distribution
])

train_dataset = datasets.EMNIST( # this is to train model, bigger version of MNIST with letters too
    root="./data",       # stores in file named data
    split="balanced",    # 47 classes, balanced mix of digits and letters so theres no bias
    train=True,          # trains model and downloads
    download=True,
    transform=transform) # apply augmentation pipeline

val_dataset = datasets.EMNIST( # separate dataset the model has never seen, used to check if its actually learning
    root="./data",
    split="balanced",
    train=False,          # uses the test split instead of training split
    download=True,
    transform=val_transform) # clean pipeline, no augmentation

num_workers = 0 if os.name == 'nt' else multiprocessing.cpu_count() # this is set to 0 specifically to avoid a windows multiprocessing bug.

train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True, num_workers=num_workers, pin_memory=True)  # 256 images per batch, num_workers=cpu cores available, pin_memory speeds up CPU->GPU transfer
val_loader = DataLoader(val_dataset, batch_size=256, shuffle=False, num_workers=num_workers, pin_memory=True)     # no shuffle for validation so results are consistent

model = CharacterCNN().to(device) # creates the model and sends it to the device (GPU or CPU)
criterion = nn.CrossEntropyLoss() # calculates how wrong the model is by comparing its output to the correct answer

checkpoint_path = "best_character_model.pth"
if os.path.exists(checkpoint_path):
    print(f"Loading existing weights from {checkpoint_path}...")
    checkpoint = torch.load(checkpoint_path, weights_only=False)
    model.load_state_dict(checkpoint["model_state"]) # load the brain from the hard drive into the model
    best_accuracy = checkpoint["accuracy"]           # load the best accuracy so we dont overwrite a better model
    print(f"Resuming from accuracy: {best_accuracy:.2f}%")
else:
    print("No saved model found. Starting from scratch!")
    best_accuracy = 0.0

optimizer = optim.Adam(model.parameters(), lr=0.0005, weight_decay=1e-5)                               # L2 regularization to prevent overfitting
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2) # reduce learning rate if validation loss doesnt improve for 2 epochs

epochs = 5 # makes the model go through the dataset 5 times


for epoch in range(epochs):

    model.train() # tells model to train
    running_loss = 0.0 # starts loss count from 0
    correct = 0 # starts correct count from 0
    total = 0 # starts total count from 0

    for images, labels in train_loader: # takes 256 images per batch
        images, labels = images.to(device), labels.to(device) # decides what device to use

        optimizer.zero_grad()              # clears the old errors
        outputs = model(images)            # sends images through
        loss = criterion(outputs, labels)  # checks answers
        loss.backward()                    # weighs how wrong it was
        optimizer.step()                   # changes parameter to get right next time

        running_loss += loss.item()                    # adds error loss weight and sees total
        _, predicted = torch.max(outputs.data, 1)     # figures out what the model thinks it is
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    epoch_accuracy = 100 * correct / total         # figures out accuracy of model
    epoch_loss = running_loss / len(train_loader)  # figures out loss of model

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
    val_loss = val_loss / len(val_loader)           # figures out validation loss

    scheduler.step(val_loss)               # modulates learning rate based on validation loss
    current_lr = scheduler.get_last_lr()[0] # gets current learning rate

    print(f"\nDevice: {device}")
    print(f"Learning Rate: {current_lr}")
    print(f"Epoch {epoch+1}\n | Train Loss: {epoch_loss:.4f}, Train Acc: {epoch_accuracy:.2f}%\n | Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.2f}%")

    if val_accuracy > best_accuracy: # if the model is better than the last one it saves it
        best_accuracy = val_accuracy
        torch.save({
            "model_state": model.state_dict(), # save the weights
            "accuracy": best_accuracy          # save the accuracy for next run
        }, "best_character_model.pth")
        print("------------------------ Breakthrough! Saved improved model! ------------------------")

print("\nTraining complete!")