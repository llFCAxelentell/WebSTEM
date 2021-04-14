from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from . models import Reto
from django.views.decorators.csrf import csrf_exempt
from json import loads

from . models import User
from . models import Session
from . models import Try
from . models import Day


# Create your views here.

def index(request):
    return render(request, 'index.html')

def juego(request):
    return render(request, 'juego.html')

def estadistica(request):
    return render(request, 'estadistica.html')

def stem(request):
    return render(request, 'stem.html')

@csrf_exempt
def SendLoginData(request):

    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    jugador_nombre = body['data_a']
    #falta lo de data_b
    jugador_objeto = User.objects.filter(username=jugador_nombre)#select * from Reto where nombre = jugador_nombre
    jugador_json = serializers.serialize('json',jugador_objeto)

    nombreBD = jugador_objeto[0].username
    passBD = jugador_objeto[0].password
    idBD = jugador_objeto[0].idd
    #if nombreBD= jugador_nombre:

    user= {
            "id":idBD
            }
    #else:
        #user= {
                #"id":-1
                #}
    return HttpResponse(idBD, content_type = "text/json-comment-filtered")

@csrf_exempt
def StartSession(request):
    '''
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    jugador_nombre = body['started']
    #falta lo de dice out of range
    jugador_objeto = Session.objects.filter(started=jugador_nombre)#select * from Reto where nombre = jugador_nombre
    jugador_json = serializers.serialize('json',jugador_objeto)

    user_idBD = jugador_objeto[0].user_id
    startedBD = jugador_objeto[0].started
    idBD = jugador_objeto[0].idd

'''
    user= {
            "id":200
            #"user":3,
            #"started":4
            }

    return HttpResponse(200, content_type = "text/json-comment-filtered")

@csrf_exempt
def AddTry(request):
    '''
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    jugador_nombre = body['debt']
    #falta lo de dice out of range
    jugador_objeto = Try.objects.filter(debt=jugador_nombre)#select * from Reto where nombre = jugador_nombre
    jugador_json = serializers.serialize('json',jugador_objeto)

    debt_idBD = jugador_objeto[0].debt
    sessionBD = jugador_objeto[0].session_id
'''
    sessio= {
            "id":300
            #"debt":1,
            #"session":2
            }

    return HttpResponse(300, content_type = "text/json-comment-filtered")

@csrf_exempt
def AddDay(request):
    session= {
            "Nada":400

            }
    return HttpResponse(400, content_type = "text/json-comment-filtered")

@csrf_exempt
def UpdateTry(request):
    session= {
            "Nada":500

            }
    return HttpResponse(500, content_type = "text/json-comment-filtered")

@csrf_exempt
def UpdateSession(request):
    session= {
            "Nada":600

            }
    return HttpResponse(600, content_type = "text/json-comment-filtered")

@login_required
def minutosJugador(request):
    usuario = request.user
    registros = Minutos.objects.filter(jugador=usuario)
    minutos = registros[0].minutos
    return render(request,'minutosJugador.html',{'minutos':minutos} )
