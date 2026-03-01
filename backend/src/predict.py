import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import string
import torchvision.transforms.functional as F
from model import CharacterCNN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")# intialize what device to use 

model = CharacterCNN().to(device)
model.load_state_dict(torch.load("character_model.pth", map_location=device))
model.eval() #load in the model 
print("Model loaded successfully")

classes = list(string.digits + string.ascii_uppercase) # intialize maps 

class InvertColor(object):
    def __call__(self, img):
        return F.invert(img)
    
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    InvertColor(), # This will flip the image and change the whites to blacks and vice versa
    transforms.ToTensor(), #process the image
    transforms.Normalize((0.5,), (0.5,))  #Normalize to match training transform 
])

def predict(image_path): # guess the image 
    image = Image.open(image_path)
    image = transform(image)
    image = image.unsqueeze(0).to(device)  

    with torch.no_grad():
        output = model(image)

        #Convert raw scores to probabilities using softmax
        #this lets us see how confident the model is, not just what it picked
        probabilities = F.softmax(output, dim=1)

        #Get top 3 guesses instead of just 1
        top3_probs, top3_indices = torch.topk(probabilities, 3, dim=1)

        _, predicted = torch.max(output, 1)

    predicted_class = predicted.item()

    if predicted_class < len(classes):
        result = classes[predicted_class]
    else:
        result = "Unknown"

    print("Prediction:", result)
    #Print top 3 predictions with confidence percentages
    #Useful for catching cases where 2 letters look similar (like 'O' vs '0')
    print("Top 3 guesses:")
    for i in range(3):
        idx = top3_indices[0][i].item()
        prob = top3_probs[0][i].item() * 100
        label = classes[idx] if idx < len(classes) else "Unknown"
        print(f"  #{i+1}: '{label}'  ({prob:.1f}% confidence)")
    return result

if __name__ == "__main__": #only runs code if use this file to run specifically 
    image_path = "Image.png"  # Change this to your image named file 

    predict(image_path)
    #updating predict file
