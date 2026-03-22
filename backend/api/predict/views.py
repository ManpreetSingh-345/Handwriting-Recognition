from __future__ import annotations
from src import predict
from PIL import Image, ImageOps
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile


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
        image_file: InMemoryUploadedFile | UploadedFile = request.FILES.get(
            'image')
        
        result = predict.predict(image_file.file)

        return JsonResponse({"Result": result})
