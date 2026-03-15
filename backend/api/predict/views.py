from django.shortcuts import render, HttpResponse
import json
import os
from src import predict
from pathlib import Path
from PIL import Image, ImageOps

print(os.getcwd())

# Open the image
image_path = "./predict/Image2.png" 

img = Image.open(image_path)
raw_image = ImageOps.exif_transpose(img)

# Create your views here.
def predictRoute(response):
    result = predict.predict(raw_image)
    jsonResult = {"character_result": f"{result}"}
    return HttpResponse(jsonResult)