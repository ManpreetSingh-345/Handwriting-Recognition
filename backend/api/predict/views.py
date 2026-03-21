from django.shortcuts import render, HttpResponse
import json
import os
from src import predict
from pathlib import Path
from PIL import Image, ImageOps
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import JsonResponse


@ensure_csrf_cookie
def get_csrf_token(request):
    # This function forces Django to set the 'csrftoken' cookie
    return JsonResponse({'detail': 'CSRF cookie set'})


# Open the image
image_path = "./predict/Image3.jpeg"

img = Image.open(image_path)
raw_image = ImageOps.exif_transpose(img)


@ensure_csrf_cookie
def predictRoute(request):
    if (request.method == "POST"):
        print(request.POST)
        result = predict.predict(raw_image)
        jsonResult = {"character_result": f"{result}"}
        return HttpResponse(result)
