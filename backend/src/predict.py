import torch
from PIL import Image
from model import CharacterCNN
from preprocess import transform 

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

# Load the blueprint and the best weights
model = CharacterCNN().to(device)
checkpoint = torch.load("best_character_model.pth", map_location=device, weights_only=False)
model.load_state_dict(checkpoint["model_state"])
model.eval() 
print("Model loaded successfully!")

# EMNIST 'balanced' exactly 47 characters
emnist_mapping = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt"
classes = list(emnist_mapping) 

def predict(image_path): 
    print(f"\nAnalyzing '{image_path}'...")
    
    # 1. Load the raw image
    raw_image = Image.open(image_path)
    
    # 2. Process it using your custom external module!
    processed_image = transform(raw_image)
    
    # 3. Add batch dimension and send to GPU/CPU
    tensor_image = processed_image.unsqueeze(0).to(device)  

    with torch.no_grad():
        output = model(tensor_image)

        # Calculate probabilities for the Top 3 Guesses
        probabilities = torch.softmax(output, dim=1)
        top3_probs, top3_indices = torch.topk(probabilities, 3, dim=1)
        _, predicted = torch.max(output, 1)

    predicted_class = predicted.item()

    if predicted_class < len(classes):
        result = classes[predicted_class]
    else:
        result = "Unknown"

    print(f"--> Final Prediction: {result} <--\n")
    
    print("Top 3 Guesses:")
    for i in range(3):
        idx = top3_indices[0][i].item()
        prob = top3_probs[0][i].item() * 100
        label = classes[idx] if idx < len(classes) else "Unknown"
        print(f"  #{i+1}: '{label}'  ({prob:.1f}% confidence)")
        
    return result

if __name__ == "__main__": 
    image_path = "/Users/zeroascend/Documents/Project/Handwriting-Recognition/backend/src/Image3.png"  
    
    try:
        predict(image_path)
    except FileNotFoundError:
        print(f"Error: Could not find '{image_path}'. Check your file path!")
