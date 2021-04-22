from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime as dt
from django.db.models import F, Func, Count
from . models import Sesion
from django.views.decorators.csrf import csrf_exempt
from json import loads, dumps
from . models import Usuario
from . models import Try
from . models import Day
from hashlib import md5


@csrf_exempt
def formulario(request):
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    edad = request.POST['edad']
    genero = request.POST['genero']
    correo = request.POST['correo']
    contrasena = request.POST['contrasena']
    pwd = md5( contrasena.encode("utf-8") ).hexdigest()
    nickname = request.POST['nickname']

    if (nombre == "" or apellido == "" or edad == "" or genero == "" or correo == "" or contrasena == "" or nickname == ""):
        return render(request, 'juego.html')
    else:
        guardar = Usuario(names= nombre, last_names=apellido, created= dt.now(), email= correo, password=pwd,username= nickname, gender= genero, birthdate= edad)
        guardar.save()
        return render(request, 'juego.html')

def index(request):
    return render(request, 'index.html')

def juego(request):
    return render(request, 'juego.html')

def estadistica(request):
    data = []
    data.append(['num_compounds_made', 'num_compounds_sold'])

    resultados= Day.objects.all()
    titulo ='compounds made vs sold'
    titulo_formato = dumps(titulo)
    if len(resultados)>0:
        for registro in resultados:
            nombre = registro.num_compounds_made
            minutos = registro.num_compounds_sold
            data.append([nombre, minutos])
        print (data)
        data_formato=dumps(data) #formatear los datos en string para json
        return render(request, 'estadistica.html', {'losDatos':data_formato}) # scatter.html
    else:
        return HttpResponse("<h1>No hay registros </h1>")
    return render(request, 'estadistica.html')

def stem(request):
    return render(request, 'stem.html')

def scatter(request):
    '''
    data = [
            ['nivel', 'exito'],
            [ 1,      90],
            [ 2,      80],
            [ 3,     75],
            [ 4,      50],
            [ 5,      45],
            [ 6,    30]
            ]
    '''
    data = []
    data.append(['num_compounds_made', 'num_compounds_sold'])

    resultados= Day.objects.all()
    titulo ='compounds made vs sold'
    titulo_formato = dumps(titulo)
    if len(resultados)>0:
        for registro in resultados:
            nombre = registro.num_compounds_made
            minutos = registro.num_compounds_sold
            data.append([nombre, minutos])
        print (data)
        data_formato=dumps(data) #formatear los datos en string para json
        return render(request, 'scatter.html', {'losDatos':data_formato}) # scatter.html
    else:
        return HttpResponse("<h1>No hay registros </h1>")
#falta verificar password

@csrf_exempt
def SendLoginData(request):

    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    jugador_nombre = body['data_a']
    jugador_pass = body['data_b']
    print(jugador_pass)
    jugador_objeto = Usuario.objects.filter(username=jugador_nombre)#select * from Reto where nombre = jugador_nombre
    jugador_json = serializers.serialize('json',jugador_objeto)

    nombreBD = jugador_objeto[0].username
    passBD = jugador_objeto[0].password
    idBD = jugador_objeto[0].id
    if passBD==jugador_pass:
        return HttpResponse(idBD)
    else:
        return HttpResponse(-1)


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


#Listo
@csrf_exempt
def AddDay(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

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


@csrf_exempt
def minutosJugadosPromedio(request):
        tiempo=0
        minutosTotales=0
        star = Sesion.objects.values_list('started', flat=True)
        end = Sesion.objects.values_list('ended', flat=True)
        minutosTotales =0.0
        for i in range(len(star)):
            tiempo = end[i] - star[i]
            minutes = tiempo.total_seconds() / 60
            minutosTotales += minutes
        prom =minutosTotales/len(star)
        return HttpResponse(prom)

@csrf_exempt
def exitoPromedio(request):
        result = (Day.objects.values('success').annotate(dcount=Count('success')).order_by())
        '''
        print("result")
        print(result)
        for i in range(len(result)):
            print(result[i])
        '''
        return HttpResponse(result)

@csrf_exempt
def scoresGlobal(request):
    p =Day.objects.select_related('try_id')
    print(p)


    return HttpResponse(100)


@csrf_exempt
def scoresGlobal5(request):
    return HttpResponse(100)

@csrf_exempt
def maxJugado(request):
    return HttpResponse(100)

@csrf_exempt
def minJugado(request):
    return HttpResponse(100)


###############estadística team

@csrf_exempt
def tiempoCompuestos(request):
    return HttpResponse(100)

@csrf_exempt
def tiempoEdad(request):
    return HttpResponse(100)

@csrf_exempt
def compuestosElementos(request):
    return HttpResponse(100)

@csrf_exempt
def nivelCompElemClieDin(request):
    return HttpResponse(100)


'''
@login_required
def minutosJugador(request):
    usuario = request.user
    registros = Minutos.objects.filter(jugador=usuario)
    minutos = registros[0].minutos
    return render(request,'minutosJugador.html',{'minutos':minutos} )
    '''
