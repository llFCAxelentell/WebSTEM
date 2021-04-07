from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

# Create your views here.

def index(request):
    return render(request, 'index.html')

def juego(request):
    return render(request, 'juego.html')

def estadistica(request):
    return render(request, 'estadistica.html')

def stem(request):
    return render(request, 'stem.html')


