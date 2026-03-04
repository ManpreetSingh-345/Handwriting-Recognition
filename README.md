# Smart Write: Handwriting Recognition

This full-stack application allows users to draw or upload images of text and accurately recognize handwriting characters using a custom Convolutional Neural Network (CNN). Made by aspiring Students.

## Features
- **Frontend App**: Interactive user interface built with modern React (Vite, Tailwind CSS v4). Features direct file uploads and UI to output predictions.
- **Deep Learning Model**: A custom Convolutional Neural Network (`CharacterCNN`) built with PyTorch.
- **47 Distinct Classes**: Capable of recognizing a combination of digits and uppercase letters natively.
- **Ready-To-Run Integration**: Contains pre-trained compiled network weights (`best_character_model.pth`) to immediately begin inferencing capabilities.
- **Optimized Training Pipeline**: Features a validation loop, learning rate scheduling, robust stateful checkpointing, and GPU/Windows compatibility fixes.

## Technology Stack

### Frontend
- **React 19 (Vite)**
- **Tailwind CSS** for aesthetic styling and animations
- **Radix UI** primitives and modular components

### Backend
- **Python / PyTorch** for the Neural Network framework
- **Torchvision** for image transformation and data normalization
- **Pillow (PIL)** for rendering and matrix processing

## Project Structure
```text
Handwriting-Recognition/
├── backend/
│   ├── src/
│   │   ├── train.py                # Pipeline script to train the CNN from scratch
│   │   ├── predict.py              # Script that loads an image and outputs inference
│   │   ├── model.py                # The CharacterCNN architecture declaration
│   │   └── best_character_model.pth# High-accuracy pre-trained CNN model
│   └── requirements.txt            # Core Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main React user interface (Smart Write)
│   │   ├── components/             # Reusable UX templates (patterns, styling plugins)
│   │   └── index.css               # Base UI tokens
│   ├── package.json                # Node environment definitions
│   └── vite.config.js              # Bundler configuration
└── README.md                       # Documentation
```

## Setup & Installation

### 1. Setting Up the Backend
We recommend running the backend inside an isolated virtual environment (`venv`) to prevent system-wide package clutter:
```bash
cd Handwriting-Recognition/backend/

# Create and execute the environment shell wrapper
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Unix/MacOS

pip install -r requirements.txt
```
*(Make sure to verify if your machine satisfies PyTorch CPU vs GPU/CUDA acceleration criteria).*

### 2. Setting Up the Frontend
You'll need `npm` and Node.js installed to build the front-facing dashboard.
```bash
cd Handwriting-Recognition/frontend/

npm install
npm run dev
```
Navigate to `http://localhost:5173/` in your browser to view the application in your local development environment.

## How to Make Predictions locally via Command Line
To test an image right away without running the full full-stack UI bridge:
1. Place a handwriting image (e.g. `Image.png`) in the `backend/src/` directory.
2. Edit `predict.py` line 48 to match your specific target image string.
3. Run the script:
   ```bash
   cd Handwriting-Recognition/backend/src
   python predict.py
   ```
The output character matching will display directly in your console.

## Convolutional Architecture Details
The machine learning component leverages a fully custom `CharacterCNN` architecture traversing via:
- **Phase 1 vision mapping**: Initial `Conv2d` applying 3x3 kernel dimension data extraction, enhanced with BatchNorm and memory-efficient `inplace` activations.
- **Max pooling matrix sizing**: Filters visual noise, stripping dimensions and resolving local maxima across 2x2 blocks.
- **Phase 2 deeper analysis**: A supplementary `Conv2d` scales down to 64 pattern-detecting output channels. 
- **Phase 3 feature extraction**: A third `Conv2d` layer scales to 128 channels before being reduced by Adaptive Average Pooling.
- **Fully Connected (FC) Network**: A 3-layer dense block progressively narrowing from 256 to 128 classifying features, leveraging Dropout for robust regularization, and outputting final geometry characteristics into 1 of 47 valid label probabilities.
  
All model predictions inject automatic grayscale mapping and inverse color transformations to reliably normalize dark-ink on bright-paper inputs.
