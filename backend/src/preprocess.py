import torchvision.transforms as transforms
from PIL import Image, ImageOps

class EMNISTFormat:
    def __call__(self, img):
        # 1. Grayscale and invert (white ink, black background)
        img = ImageOps.grayscale(img)
        img = ImageOps.invert(img)
        
        # 2. Crush the shadows (binarization)
        threshold = 100 
        img = img.point(lambda p: 255 if p > threshold else 0)
        
        # 3. Crop tightly to the letter to remove dead space
        bbox = img.getbbox()
        if bbox is None:
            return img.resize((28, 28))
        
        img_cropped = img.crop(bbox)
        
        # 4. Shrink so the longest edge is exactly 20 pixels
        img_cropped.thumbnail((20, 20), Image.Resampling.LANCZOS)
        
        # 5. Paste into the dead center of a 28x28 black canvas
        new_img = Image.new('L', (28, 28), color=0)
        paste_x = (28 - img_cropped.width) // 2
        paste_y = (28 - img_cropped.height) // 2
        new_img.paste(img_cropped, (paste_x, paste_y))
        
        return new_img

# The pipeline ready to be imported by any other file in your project!
transform = transforms.Compose([
    EMNISTFormat(), 
    transforms.ToTensor(), 
    transforms.Normalize((0.5,), (0.5,)) 
])