from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('index.html',views.index, name = 'index'),
    path('juego.html',views.juego, name = 'juego'),
    path('estadistica.html',views.estadistica, name = 'estadistica'),
    path('stem.html',views.stem, name = 'stem'),
    path('SendLoginData',views.SendLoginData, name='SendLoginData'),
    path('StartSession',views.StartSession, name='StartSession'),
    path('AddTry',views.AddTry, name='AddTry'),
    path('AddDay',views.AddDay, name='AddDay'),
    path('UpdateTry',views.UpdateTry, name='UpdateTry'),
    path('UpdateSession',views.UpdateSession, name='UpdateSession'),
    path('minutosJugadosTotales',views.minutosJugadosTotales, name='minutosJugadosTotales'),
    path('minutosJugadosPromedio',views.minutosJugadosPromedio, name='minutosJugadosPromedio'),

]
