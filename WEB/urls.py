from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('index.html',views.index, name = 'index'),
    path('juego.html',views.juego, name = 'juego'),
    path('estadistica.html',views.estadistica, name = 'estadistica'),
    path('stem.html',views.stem, name = 'stem'),
]