import torchvision.transforms as transforms
from PIL import Image, ImageOps
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion

class EMNISTFormat:
    def __call__(self, img):
        # 1. Convert to grayscale
        img = ImageOps.grayscale(img)
        img_np = np.array(img)

        # 2. Corner-based background detection (more robust than most-common-pixel)
        h, w = img_np.shape
        corners = [
            img_np[0:5, 0:5],
            img_np[0:5, w-5:w],
            img_np[h-5:h, 0:5],
            img_np[h-5:h, w-5:w]
        ]
        bg_value = np.median(np.concatenate([c.flatten() for c in corners]))

        # 3. Invert if background is light
        if bg_value > 127:
            img_np = 255 - img_np

        # 4. Add border before cropping so edge-touching letters don't break
        img_np = np.pad(img_np, pad_width=6, mode='constant', constant_values=0)

        # 5. Otsu-style adaptive binarization (handles varying contrast better)
        flat = img_np.flatten()
        threshold = np.percentile(flat[flat > 10], 40)  # ignores near-black background noise
        binary = (img_np > threshold).astype(np.uint8)

        # 6. Stroke normalization — BEFORE resizing
        stroke_density = binary.sum() / binary.size
        print(f"Stroke density: {stroke_density:.4f}")  # debug - tells you how thin

        if stroke_density > 0.3:
            binary = binary_erosion(binary, iterations=1).astype(np.uint8)
        elif stroke_density < 0.02:    # very thin like your A
            binary = binary_dilation(binary, iterations=5).astype(np.uint8)
        elif stroke_density < 0.05:    # thin like your H
            binary = binary_dilation(binary, iterations=4).astype(np.uint8)
        elif stroke_density < 0.12:
            binary = binary_dilation(binary, iterations=2).astype(np.uint8)

        img_np = (binary * 255).astype(np.uint8)
        img = Image.fromarray(img_np)
        img.save("debug_before_resize.png")

        # 7. Crop tightly to the letter
        bbox = img.getbbox()
        if bbox is None:
            return img.resize((28, 28))
        img_cropped = img.crop(bbox)

        # 8. Resize longest edge to 20px
        img_cropped = img_cropped.resize((20, 20), Image.Resampling.NEAREST)

        # 9. Re-binarize after resize (LANCZOS introduces gray anti-aliasing)
        img_np2 = np.array(img_cropped)
        img_np2 = np.where(img_np2 > 127, 255, 0).astype(np.uint8)
        img_cropped = Image.fromarray(img_np2)

        # 10. Center in 28x28 canvas
        new_img = Image.new('L', (28, 28), color=0)
        paste_x = (28 - img_cropped.width) // 2
        paste_y = (28 - img_cropped.height) // 2
        new_img.paste(img_cropped, (paste_x, paste_y))

        new_img.save("debug_processed.png")

        return new_img


transform = transforms.Compose([
    EMNISTFormat(),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])