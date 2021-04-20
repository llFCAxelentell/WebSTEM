from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime as dt
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

#falta verificar password
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

#listo
@csrf_exempt
def minutosJugadosTotales(request):
        tiempo=0
        minutosTotales=0
        star = Sesion.objects.values_list('started', flat=True)
        end = Sesion.objects.values_list('ended', flat=True)
        minutosTotales =0.0
        for i in range(len(star)):
            tiempo = end[i] - star[i]
            minutes = tiempo.total_seconds() / 60
            minutosTotales += minutes

        return HttpResponse(minutosTotales)


#Listo, solo que ahora no recivo el started, solo el id del usuario
@csrf_exempt
def StartSession(request):

    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    jugador_user_id = body['user_id']
    jugador_started = body['started']
    ahorita= dt.now()
    p = Sesion(user_id = Usuario(jugador_user_id), started=ahorita, ended=None)
    p.save()
    print(p.id)

    return HttpResponse(p.id)


#Listo
@csrf_exempt
def AddTry(request):

    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    session_id = body['session_id']
    try_num = body['try_num']

    s = Try(session_id = Sesion(session_id), try_num=try_num, debt=None)
    s.save()

    return HttpResponse(s.id)


@csrf_exempt
def AddDay(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    #falta código

    try_i =body['try_id']
    dayNumbe=body['dayNumber']
    succes =body['success']
    num_compounds_mad=body['num_compounds_made']
    num_compounds_sol=body['num_compounds_sold']
    num_elements_purchase=body['num_elements_purchased']
    customers_rejecte=body['customers_rejected']
    money_generated_da=body['money_generated_day']

    d = Day(try_id=Try(try_i), dayNumber=dayNumbe, success=succes, num_compounds_made=num_compounds_mad, num_compounds_sold=num_compounds_sol,  num_elements_purchased=num_elements_purchase, customers_rejected=customers_rejecte, money_generated_day=money_generated_da)
    d.save()

    return HttpResponse("okAddDay")

#Listo
@csrf_exempt
def UpdateTry(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    id = body['id']
    deb = body['debt']

    a= Try.objects.get(pk=id)
    a.debt= deb
    a.save()
    return HttpResponse("okUpdateTry")

#listo, solo recibo el id, el ended ya no
@csrf_exempt
def UpdateSession(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    sesion_id = body['id']
    jugador_ended = body['ended']

    a= Sesion.objects.get(pk=sesion_id)
    a.ended= dt.now()
    a.save()

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
