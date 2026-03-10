import cv2
import numpy as np
import torchvision.transforms as transforms
from PIL import Image

class EMNISTFormat:
    def __call__(self, img):
        # 1. Convert to float32
        img_np = np.array(img.convert('RGB')).astype(np.float32) 
        
        # 2. Blur to crush harsh JPEG artifacts
        blurred = cv2.GaussianBlur(img_np, (5, 5), 0)
        
        # 3. Sample the extreme edges to find the background color
        h, w, _ = blurred.shape
        border = np.concatenate([
            blurred[0:3, :].reshape(-1, 3), 
            blurred[-3:, :].reshape(-1, 3), 
            blurred[:, 0:3].reshape(-1, 3), 
            blurred[:, -3:].reshape(-1, 3)
        ])
        bg_color = np.median(border, axis=0)
        
        # 4. Measure difference & normalize
        diff = np.linalg.norm(blurred - bg_color, axis=2)
        diff_gray = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # 5. Otsu's Method
        _, binary = cv2.threshold(diff_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 6. Find boundaries
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours: 
            return Image.fromarray(np.zeros((28, 28), dtype=np.uint8))
            
        # Filter out dust by measuring height/width
        valid_contours = []
        for c in contours:
            _, _, w_c, h_c = cv2.boundingRect(c)
            if w_c > 5 or h_c > 5:
                valid_contours.append(c)
                
        if not valid_contours:
            valid_contours = contours 
            
        # Combine all valid strokes into one giant shape array
        all_points = np.vstack(valid_contours)
        x, y, w_box, h_box = cv2.boundingRect(all_points)
        
        if w_box < 2 or h_box < 2:
             return Image.fromarray(np.zeros((28, 28), dtype=np.uint8))

        cropped = binary[y:y+h_box, x:x+w_box]
        
        # Calculate exactly how severely we are shrinking this image
        scale = 20.0 / max(w_box, h_box)
        inverse_scale = max(1, int(1.0 / scale))
        
        stroke_density = np.sum(cropped > 0) / (w_box * h_box)
        
        # Dynamically build a massive dilation kernel if the image is massive
        kernel_size = max(2, int(inverse_scale * 0.5)) 
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        if stroke_density < 0.15:
            cropped = cv2.dilate(cropped, kernel, iterations=1)
        elif stroke_density > 0.60:
            cropped = cv2.erode(cropped, kernel, iterations=1)
            
        # 8. Resize longest edge to 20 pixels
        new_w, new_h = max(1, int(w_box * scale)), max(1, int(h_box * scale))
        resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # Stretches faint gray smudges back into bright white 255 ink
        resized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)
        
        # 9. Paste into canvas (Bounding Box Centering)
        canvas = np.zeros((28, 28), dtype=np.uint8)
        start_y = (28 - new_h) // 2
        start_x = (28 - new_w) // 2
        canvas[start_y:start_y+new_h, start_x:start_x+new_w] = resized
        
        # 10. Center of Mass Shift
        M = cv2.moments(canvas)
        if M["m00"] != 0:
            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]
            dx = 14.0 - cx
            dy = 14.0 - cy
            M_trans = np.float32([[1, 0, dx], [0, 1, dy]])
            canvas = cv2.warpAffine(canvas, M_trans, (28, 28))
        
        cv2.imwrite("debug_processed_opencv.png", canvas)
        return Image.fromarray(canvas)
    
transform = transforms.Compose([
    EMNISTFormat(),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])