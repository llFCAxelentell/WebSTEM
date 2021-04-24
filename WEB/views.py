from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime as dt
from django.db.models import F, Func, Count
from . models import Sesion
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from json import loads, dumps
from . models import Usuario
from . models import Try
from . models import Day
from hashlib import md5
import psycopg2
import numpy as np



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
        return render(request, 'juego.html', {'enviarInfo':"Faltan datos"})
    else:
        user = User.objects.create_user(nickname, correo, contrasena)
        user.save()
        usuarios = User.objects.filter(username = nickname)
        u=usuarios[0]

        guardar = Usuario(names= nombre, last_names=apellido, created= dt.now(), email= correo, password=pwd,username= u, gender= genero, birthdate= edad)
        guardar.save()

        return render(request, 'juego.html',{'enviarInfo':"Registrado"})

def index(request):
    return render(request, 'index.html')

def juego(request):
    return render(request, 'juego.html')

@login_required
def mi_estadistica(request):

    try:
        usuario = request.user
        #\set uu request.user
        registros = User.objects.filter(username=usuario)
        print(registros)
        regist = Usuario.objects.filter(username=registros[0].id)
        print(regist[0].gender)
        dato= regist[0].gender

        #################################
        #Minutos jugados totales
        #Duración promedio de sesión
        #Tiempo máximo de juego por sesión
        #Tiempo mínimo de juego por sesión

        tiempos = []
        star = Sesion.objects.values_list('started', flat=True)
        end = Sesion.objects.values_list('ended', flat=True)
        minutosTotales =0.0
        for i in range(len(star)):
            tiempo = end[i] - star[i]
            minutes = tiempo.total_seconds() / 60
            tiempos.append(minutes)
            minutosTotales += minutes

        maxTiempo = np.max(tiempos)
        minTiempo = np.min(tiempos)
        promTemp =minutosTotales/len(star)

        #################################

        #Compuestos vendidos vs elementos comprados
        data2 = []
        data2.append(['num_elements_purchased', 'num_compounds_sold'])
        resultados= Day.objects.all()
        for registro in resultados:
            nombre = registro.num_elements_purchased
            minutos = registro.num_compounds_sold
            data2.append([nombre, minutos])
        data2_formato=dumps(data2)
        #############

        connection = psycopg2.connect(
            user = "farmaceuticouser",
            password = "LibroVerde23",
            host = "localhost",
            port = "5432",
            database = "medchembd"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM auth_user WHERE auth_user.username =hola;")
        rows = cursor.fetchall()
        print(rows)

        '''
        data= []
        data3 =[]

        data6 = []
        data.append(['Tiempo', 'Compuestos hechos'])
        data3.append(['Nivel','Compuestos','Elementos', 'Clientes'])


        cursor = connection.cursor()
        cursor2 = connection.cursor()
        cursor3 = connection.cursor()

        cursor5 = connection.cursor()
        cursor6 = connection.cursor()
        cursor7 = connection.cursor()


        #Tiempo jugado vs compuestos hechos
        cursor.execute("SELECT extract (epoch from (ended::timestamp - started::timestamp))::integer/60 AS TiempoSesion FROM \"WEB_sesion\";")
        cursor2.execute("SELECT SUM(num_compounds_made) FROM \"WEB_day\" INNER JOIN \"WEB_try\" ON \"WEB_day\".try_id_id=\"WEB_try\".id INNER JOIN \"WEB_sesion\" ON \"WEB_try\".session_id_id= \"WEB_sesion\".id GROUP BY \"WEB_try\".session_id_id;")

        #Nivel vs (compuestos, elementos, clientes, dinero)
        #la gigante
        cursor3.execute("SELECT day_number, AVG(num_compounds_sold) AS PromCompuestosVendidos, AVG(num_elements_purchased) AS PromElementos, AVG(customers_rejected) AS PromClientesRechazados FROM \"WEB_day\" GROUP BY day_number;") #


        #Promedio de éxito / fallo por nivel
        cursor5.execute("SELECT day_number, avg(success::int) AS PromedioExito FROM \"WEB_day\" GROUP BY day_number;")

        #Top five de scores
        cursor6.execute("SELECT auth_user.username, (AVG(money_generated_day)*MAX(day_number)) AS Score FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id GROUP BY username ORDER BY Score DESC LIMIT 5 ;")
        #Top score global
        cursor7.execute("SELECT auth_user.username, (AVG(money_generated_day)*MAX(day_number)) AS Score FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id GROUP BY username ORDER BY Score DESC LIMIT 1 ;")


        rows = cursor.fetchall()
        rows2= cursor2.fetchall()
        rows3= cursor3.fetchall()
        rows5= cursor5.fetchall()
        rows6= cursor6.fetchall()
        rows7= cursor7.fetchall()

        #print(rows3)
        #print(rows6)
        ota= []
        ota2=[]
        for row in rows:
            ota.append(row[0])
        for rowe in rows2:
            ota2.append(rowe[0])

        for roweee in rows3:
            data3.append([int(roweee[0]), int(roweee[1]), int(roweee[2]), int(roweee[3])])

        data3_formato = dumps(data3)



        contador = 1
        for roowe in rows6:
            data6.append([contador, roowe[0], int(roowe[1]) ])
            contador = contador+1
        data6_formato= dumps(data6)

        for i in range(len(ota)):
            data.append([ota[i], ota2[i]])

        data_formato= dumps(data)
            #totales += row[2]
            '''
    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is now closed")


    return render(request, 'mi_estadistica.html', {'dato':dato})
'''
def estadistica(request):
#grafica compounds made vs sold
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
        data_formato=dumps(data) #formatear los datos en string para json
        #return render(request, 'estadistica.html', {'losDatos':data_formato}) # scatter.html
    else:
        return HttpResponse("<h1>No hay registros </h1>")

# grafica num_compounds_made
    data1 = []
    tiempo=0
    resultados1 = (Day.objects.values('try_id').annotate(dcount=Count('num_compounds_made')).order_by())
    print(resultados1)
    star = Sesion.objects.values_list('started', flat=True)
    end = Sesion.objects.values_list('ended', flat=True)
    for i in range(len(star)):
        tiempo = end[i] - star[i]
        minutes = tiempo.total_seconds() / 60
        data1.append([minutes])

    return render(request, 'estadistica.html', {'losDatos':data_formato})
    #return render(request, 'estadistica.html')
'''
def stem(request):
    return render(request, 'stem.html')
'''
def scatter(request):

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
'''

@csrf_exempt
def SendLoginData(request):

    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    jugador_nombre = body['data_a']
    jugador_pass = body['data_b']

    jugador_o  = User.objects.filter(username=jugador_nombre)
    jugador_objeto = Usuario.objects.filter(username=jugador_o[0].id)#select * from Reto where nombre = jugador_nombre

    passBD = jugador_objeto[0].password
    idBD = jugador_objeto[0].id
    print(passBD)
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
    day_numbe=body['day_number']
    succes =body['success']
    num_compounds_mad=body['num_compounds_made']
    num_compounds_sol=body['num_compounds_sold']
    num_elements_purchase=body['num_elements_purchased']
    customers_rejecte=body['customers_rejected']
    money_generated_da=body['money_generated_day']

    d = Day(try_id=Try(try_i), day_number=day_numbe, success=succes, num_compounds_made=num_compounds_mad, num_compounds_sold=num_compounds_sol,  num_elements_purchased=num_elements_purchase, customers_rejected=customers_rejecte, money_generated_day=money_generated_da)
    d.save()

    return HttpResponse("okAddDay")

#Listo
@csrf_exempt
def UpdateTry(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    idd = body['id']
    deb = body['debt']

    a= Try.objects.get(pk=idd)
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

@csrf_exempt
def estadistica(request):

    try:
        #################################
        #Minutos jugados totales
        #Duración promedio de sesión
        #Tiempo máximo de juego por sesión
        #Tiempo mínimo de juego por sesión

        tiempos = []
        star = Sesion.objects.values_list('started', flat=True)
        end = Sesion.objects.values_list('ended', flat=True)
        minutosTotales =0.0
        for i in range(len(star)):
            tiempo = end[i] - star[i]
            minutes = tiempo.total_seconds() / 60
            tiempos.append(minutes)
            minutosTotales += minutes

        maxTiempo = np.max(tiempos)
        minTiempo = np.min(tiempos)
        promTemp =minutosTotales/len(star)

        #################################

        #Compuestos vendidos vs elementos comprados
        data2 = []
        data2.append(['num_elements_purchased', 'num_compounds_sold'])
        resultados= Day.objects.all()
        for registro in resultados:
            nombre = registro.num_elements_purchased
            minutos = registro.num_compounds_sold
            data2.append([nombre, minutos])
        data2_formato=dumps(data2)
        #############

        connection = psycopg2.connect(
            user = "farmaceuticouser",
            password = "LibroVerde23",
            host = "localhost",
            port = "5432",
            database = "medchembd"
        )

        data= []
        data3 =[]
        data4= []
        data6 = []
        data.append(['Tiempo', 'Compuestos hechos'])
        data3.append(['Nivel','Compuestos','Elementos', 'Clientes'])
        data4.append(['Edad', 'Tiempo'])

        cursor = connection.cursor()
        cursor2 = connection.cursor()
        cursor3 = connection.cursor()
        cursor4 = connection.cursor()
        cursor5 = connection.cursor()
        cursor6 = connection.cursor()
        cursor7 = connection.cursor()


        #Tiempo jugado vs compuestos hechos
        cursor.execute("SELECT extract (epoch from (ended::timestamp - started::timestamp))::integer/60 AS TiempoSesion FROM \"WEB_sesion\";")
        cursor2.execute("SELECT SUM(num_compounds_made) FROM \"WEB_day\" INNER JOIN \"WEB_try\" ON \"WEB_day\".try_id_id=\"WEB_try\".id INNER JOIN \"WEB_sesion\" ON \"WEB_try\".session_id_id= \"WEB_sesion\".id GROUP BY \"WEB_try\".session_id_id;")

        #Nivel vs (compuestos, elementos, clientes, dinero)
        #la gigante
        cursor3.execute("SELECT day_number, AVG(num_compounds_sold) AS PromCompuestosVendidos, AVG(num_elements_purchased) AS PromElementos, AVG(customers_rejected) AS PromClientesRechazados FROM \"WEB_day\" GROUP BY day_number;") #

        #Edad vs tiempo jugado
        cursor4.execute("SELECT  DATE_PART('year', CURRENT_DATE::date) - DATE_PART('year', birthdate::date) AS Edad, avg(extract (epoch from (ended::timestamp - started::timestamp))::integer/60) AS Tiempo FROM \"WEB_sesion\" INNER JOIN \"WEB_usuario\" ON \"WEB_sesion\".user_id_id=\"WEB_usuario\".id GROUP BY Edad ;") #

        #Promedio de éxito / fallo por nivel
        cursor5.execute("SELECT day_number, avg(success::int) AS PromedioExito FROM \"WEB_day\" GROUP BY day_number;")

        #Top five de scores
        cursor6.execute("SELECT auth_user.username, (AVG(money_generated_day)*MAX(day_number)) AS Score FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id GROUP BY username ORDER BY Score DESC LIMIT 5 ;")
        #Top score global
        cursor7.execute("SELECT auth_user.username, (AVG(money_generated_day)*MAX(day_number)) AS Score FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id GROUP BY username ORDER BY Score DESC LIMIT 1 ;")


        rows = cursor.fetchall()
        rows2= cursor2.fetchall()
        rows3= cursor3.fetchall()
        rows4= cursor4.fetchall()
        rows5= cursor5.fetchall()
        rows6= cursor6.fetchall()
        rows7= cursor7.fetchall()

        #print(rows3)
        #print(rows6)
        ota= []
        ota2=[]
        for row in rows:
            ota.append(row[0])
        for rowe in rows2:
            ota2.append(rowe[0])

        for roweee in rows3:
            data3.append([int(roweee[0]), int(roweee[1]), int(roweee[2]), int(roweee[3])])

        data3_formato = dumps(data3)

        for rowee in rows4:
            data4.append([int(rowee[0]), int(rowee[1])])
        data4_formato = dumps(data4)

        contador = 1
        for roowe in rows6:
            data6.append([contador, roowe[0], int(roowe[1]) ])
            contador = contador+1
        data6_formato= dumps(data6)

        for i in range(len(ota)):
            data.append([ota[i], ota2[i]])

        data_formato= dumps(data)
            #totales += row[2]

    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is now closed")

    return render(request, 'estadistica.html', {'losDatos':data_formato,'losDatos2':data2_formato, 'losDatos4':data4_formato, 'losDatos3':data3_formato, 'losDatos6':data6_formato,'minutosTotales':str(round(minutosTotales, 2)) ,'promTemp':str(round(promTemp, 2)), 'maxTiempo':str(round(maxTiempo, 2)), 'minTiempo':str(round(minTiempo, 2))})


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
