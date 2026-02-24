import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import string
from model import CharacterCNN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")# intialize what device to use 

model = CharacterCNN().to(device)
model.load_state_dict(torch.load("character_model.pth", map_location=device))
model.eval() #load in the model 
print("Model loaded successfully")

classes = list(string.digits + string.ascii_uppercase) # intialize maps 

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),]) #process the image 

def predict(image_path): # guess the image 
    image = Image.open(image_path)
    image = transform(image)
    image = image.unsqueeze(0).to(device)  

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)

    predicted_class = predicted.item()

    if predicted_class < len(classes):
        result = classes[predicted_class]
    else:
        result = "Unknown"

    print("Prediction:", result)
    return result

if __name__ == "__main__": #only runs code if use this file to run specifically 
    image_path = ""  # Change this to your image named file 

    predict(image_path)
    #updating predict file