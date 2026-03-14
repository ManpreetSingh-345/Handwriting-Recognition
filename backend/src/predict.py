import os
import torch
import numpy as np
from PIL import Image, ImageOps
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

#-- Rejection Implementation-- 
CONFIDENCE_REJECT   = 10.0   # below this % = always reject, definitely not a character
CONFIDENCE_WARN     = 40.0   # below this % = warn user but still give best guess
GAP_REJECT          = 5.0    # if top 2 guesses are within this % of each other = always reject, probably not a clear character
INK_MIN             = 0.02   # processed image must have at least 2% white pixels, as anything less is probably ablank canvas or a tiny scribble 
INK_MAX             = 0.95   # processed image must have less than 95% white pixels as anything more means inversion probably failed


#-- Image Checker --
def check_image_quality(processed_tensor):  
    # Un-normalize from [-1,1] back to [0,1]  
    img_np = (processed_tensor.squeeze().numpy() * 0.5) + 0.5  

    ink_ratio = np.mean(img_np > 0.5)  # fraction of pixels that are "ink" (bright)  

    if ink_ratio < INK_MIN:  
        return False, f"Image is nearly blank (ink coverage: {ink_ratio*100:.1f}%) — looks like a scribble or empty image"  
    if ink_ratio > INK_MAX: 
        return False, f"Image is almost entirely white (ink coverage: {ink_ratio*100:.1f}%) — background detection may have failed"  

    return True, "OK"  


def predict(image_path): 
    print(f"\nAnalyzing '{image_path}'...")
    
    # 1. Load the raw image
    raw_image = Image.open(image_path)
    
    # Forces Python to physically rotate the image if a smartphone saved it sideways
    raw_image = ImageOps.exif_transpose(raw_image)
    
    # 2. Process it using your custom external module!
    processed_image = transform(raw_image)
    
    #Image quality check (before model even runs) 
    is_valid, reason = check_image_quality(processed_image)  
    if not is_valid: 
        print(f" REJECTED (bad image): {reason}") 
        return None 
    
    # 3. Add batch dimension and send to GPU/CPU
    tensor_image = processed_image.unsqueeze(0).to(device)  

    with torch.no_grad():
        output = model(tensor_image)

        # Calculate probabilities for the Top 3 Guesses
        probabilities = torch.softmax(output, dim=1)
        top3_probs, top3_indices = torch.topk(probabilities, 3, dim=1)
        
        predicted = top3_indices[0][0].item()
        confidence = top3_probs[0][0].item()*100
        second_conf = top3_probs[0][1].item() * 100  
        result = classes[predicted]
    gap = confidence - second_conf # how much more confident the model is in its top guess compared to the second guess

    #Confidence-based rejection
    if confidence < CONFIDENCE_REJECT: 
        print(f"REJECTED (too uncertain): {confidence:.1f}% confidence, character not identifiable") 
        return None  

    #Confusion check 
    if confidence < CONFIDENCE_WARN and gap < GAP_REJECT:  #if low confidence and model is split between two options
        print(f"REJECTED (model confused): Top guess '{result}' at {confidence:.1f}%, "  
              f"but #2 is only {gap:.1f}% behind — too close to call")  
        return None  
    

    print(f"--> Final Prediction: {result} <--\n")
    
    print("Top 3 Guesses:")
    for i in range(3):
        idx = top3_indices[0][i].item()
        prob = top3_probs[0][i].item() * 100
        label = classes[idx] if idx < len(classes) else "Unknown"
        print(f"  #{i+1}: '{label}'  ({prob:.1f}% confidence)")
        

        
    return result

def predict_folder(folder_path):  
    SUPPORTED = (".png", ".jpg", ".jpeg")  #the file types that will be processed 
    results = {}  #stores results in a dictionary 

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(SUPPORTED)]  #scans folder to create list of the supported files listed above and makes sure capitalization doesn't cause any issues, and makes sure the file names end with the supported files.
    if not files:  #checks to see if there are none
        print("No supported files found in folder.")  
        return  

    print(f"\n Number of total files in folder: {len(files)} being processed...\n")  

    for filename in files:  
        full_path = os.path.join(folder_path, filename)  
        result = predict(full_path)  #runs existing predict on each file
        results[filename] = result  

    print("\n--FOLDER RESULTS--")  
    for name, prediction in results.items():  
        status = prediction if prediction else "Rejection"  
        print(f"  {name}  ->  {status}")  
    print("-------------------\n")  
    return results 

if __name__ == "__main__":
    try:
        predict_folder("/Users/lodrr/python-projects/Handwriting-Recognition-1/backend/src/newfolder")
    except FileNotFoundError:
        print("Error: Could not find folder. Check your folder path!")
    
    image_path = "./Image2.png" 
    try:
        predict(image_path)
    except FileNotFoundError:
        print(f"Error: Could not find '{image_path}'. Check your file path!")

