from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime
from django.db.models import F, Func
from . models import Sesion
from django.views.decorators.csrf import csrf_exempt
from json import loads

from . models import Usuario

from . models import Try
from . models import Day


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
    jugador_pass = body['data_b']
    jugador_objeto = Usuario.objects.filter(username=jugador_nombre)#select * from Reto where nombre = jugador_nombre
    jugador_json = serializers.serialize('json',jugador_objeto)

    nombreBD = jugador_objeto[0].username
    passBD = jugador_objeto[0].password
    idBD = jugador_objeto[0].id

    #FALTA VALIDAR LOS DATOS CON UN IF

    return HttpResponse(idBD)

@csrf_exempt
def minutosJugadosTotales(request):
        '''
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        startedMin = body['started']
        startedMin2 = Sesion.objects.filter(started=startedMin)
        endedMin = body['ended']
        endedMin2 = Sesion.objects.filter(ended=endedMin)
        FMT = '%Y/%m/%d, %H:%M:%S'
        dif = (datetime.strptime(startedMin2,FMT)-datetime.strptime(endedMin2,FMT))/60
        segundos = dif.total_seconds()
        SumaMinutos = sum(round(segundos))
        SumaMinutos_json = serializers.serialize('json',SumaMinnutos)
        '''

        tiempo=0
        minutosTotales=0
        star = Sesion.objects.values_list('started', flat=True)
        end = Sesion.objects.values_list('ended', flat=True)
        #star= Sesion.objects.values('started')
        #end= Sesion.objects.values('ended')
        print(star)
        print(end)
        #aa=Sesion.objects.annotate(duration = Func(F('ended'), F('started'), function='year'))
        #print(aa)

        for i in range(len(star)):
            print("end ")
            print(end[i])
            print("star ")
            print(star[i])

            tiempo = end[i] - star[i]
            print(tiempo)
            #last_datetime__lt=now + datetime.timedelta(seconds=1)*F("interval"))
            #minutosTotales += tiempo

        return HttpResponse(5000)



@csrf_exempt
def StartSession(request):

    '''
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    jugador_user_id = body['user_id']
    jugador_started = body['started']

    p = Sesion(user_id = Usuario(jugador_user_id), started=jugador_started, ended=False)
    p.save()
    jugador_objeto = Sesion.objects.filter(user_id=jugador_user_id)
    jugador_json = serializers.serialize('json',jugador_objeto)

    user_idBD = jugador_objeto[0].user_id
    startedBD = jugador_objeto[0].started
    idBD = jugador_objeto[0].id


    user= {
            "id":200
            #"user":3,
            #"started":4
            }

    '''
    return HttpResponse(200)


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


    return HttpResponse(300)

@csrf_exempt
def AddDay(request):
    #falta código
    return HttpResponse("okAddDay")

@csrf_exempt
def UpdateTry(request):
    #falta código
    return HttpResponse("okUpdateTry")

@csrf_exempt
def UpdateSession(request):
    #falta código
    return HttpResponse("okUpdateSession")

    #a esto no le tomes ss, plox
'''
@login_required
def minutosJugador(request):
    usuario = request.user
    registros = Minutos.objects.filter(jugador=usuario)
    minutos = registros[0].minutos
    return render(request,'minutosJugador.html',{'minutos':minutos} )
    '''
