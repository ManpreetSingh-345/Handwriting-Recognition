import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import torchvision.transforms.functional as F
from torch.utils.data import DataLoader
from model import CharacterCNN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 

transform = transforms.Compose([ # Custom pipeline to match EMNIST formatting
    transforms.Grayscale(num_output_channels=1),
    transforms.Lambda(lambda img: F.rotate(img, -90, fill=0)), 
    transforms.Lambda(lambda img: F.hflip(img)),               
    transforms.RandomAffine(degrees=15, translate=(0.1, 0.1), scale=(0.8, 1.2)), 
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,)) 
])

train_dataset = datasets.EMNIST(
    root="./data",              
    split="balanced",           
    train=True,                 
    download=True,
    transform=transform) 

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True) 

model = CharacterCNN().to(device)
criterion = nn.CrossEntropyLoss()

checkpoint_path = "best_character_model.pth"
if os.path.exists(checkpoint_path):
    print(f"Loading existing weights from {checkpoint_path}...")
    # Load the brain from the hard drive into the model
    model.load_state_dict(torch.load(checkpoint_path, weights_only=True))
else:
    print("No saved model found. Starting from scratch!")

optimizer = optim.Adam(model.parameters(), lr=0.0005, weight_decay=1e-5) # L2 regularization to prevent overfitting
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)# Reduce learning rate if validation loss doesn't improve for 2 epochs

epochs = 5 
best_accuracy = 0.0 

for epoch in range(epochs):
    model.train() 
    running_loss = 0.0 
    correct = 0 
    total = 0 

    for images, labels in train_loader: 
        images, labels = images.to(device), labels.to(device) 

        optimizer.zero_grad() 
        outputs = model(images) 
        loss = criterion(outputs, labels) 
        loss.backward() 
        optimizer.step() 
        running_loss += loss.item() 
        _, predicted = torch.max(outputs.data, 1) 
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    epoch_accuracy = 100 * correct / total 
    epoch_loss = running_loss / len(train_loader) 

    scheduler.step(epoch_loss) 
    
    current_lr = optimizer.param_groups[0]['lr']
    
    print(f"\nDevice: {device}")
    print(f"Learning Rate: {current_lr}")
    print(f"Epoch {epoch+1}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.2f}%") 
    
    if epoch_accuracy > best_accuracy: 
        best_accuracy = epoch_accuracy
        torch.save(model.state_dict(), "best_character_model.pth")
        print("  -> Saved improved model!")

print("\nTraining complete!")   