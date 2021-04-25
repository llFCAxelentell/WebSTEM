from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('index.html',views.index, name = 'index'),
    path('juego.html',views.juego, name = 'juego'),
    path('estadistica.html',views.estadistica, name = 'estadistica'),
    path('mi_estadistica.html',views.mi_estadistica, name = 'mi_estadistica'),
    path('stem.html',views.stem, name = 'stem'),
    path('SendLoginData',views.SendLoginData, name='SendLoginData'),
    path('StartSession',views.StartSession, name='StartSession'),
    path('AddTry',views.AddTry, name='AddTry'),
    path('AddDay',views.AddDay, name='AddDay'),
    path('UpdateTry',views.UpdateTry, name='UpdateTry'),
    path('UpdateSession',views.UpdateSession, name='UpdateSession'),
    path('minutosJugadosTotales',views.minutosJugadosTotales, name='minutosJugadosTotales'),
    path('minutosJugadosPromedio',views.minutosJugadosPromedio, name='minutosJugadosPromedio'),
    

    #path('scatter',views.scatter, name='scatter'),
    #path('minutosTotales',views.minutosTotales, name='minutosTotales'),
    path('formulario',views.formulario, name='formulario'),

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
