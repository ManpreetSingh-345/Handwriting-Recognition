from django.shortcuts import render, HttpResponse
import json
from src import predict

# Create your views here.
def predict(respone):
    return HttpResponse("Loaded")