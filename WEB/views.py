from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime as dt
from datetime import timedelta
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
        uuu = str(usuario)
        uu ="\'"+uuu+"\'"
        print(uu)

        registros = User.objects.filter(username=usuario)
        regist = Usuario.objects.filter(username=registros[0].id)
        dato= regist[0].gender

        connection = psycopg2.connect(
            user = "farmaceuticouser",
            password = "LibroVerde23",
            host = "localhost",
            port = "5432",
            database = "medchembd"
        )
        data6=[]
        data7=[]
        data9=[]
        data8=[]
        data10=[]
        data6.append(['nivel', 'exito'])
        data7.append(['tiempo', 'compuestos'])
        data9.append(['compuestos', 'elementos'])
        data10.append(['nivel', 'compuestos', 'elementos', 'clientes'])

        cursor = connection.cursor()
        cursor2 = connection.cursor()
        cursor3 = connection.cursor()
        cursor4 = connection.cursor()
        cursor5 = connection.cursor()
        cursor6 = connection.cursor()
        cursor7 = connection.cursor()
        cursor8 = connection.cursor()
        cursor9 = connection.cursor()
        cursor10 = connection.cursor()

        #Tiempo y nivel
        myQuery="SELECT sum(extract (epoch from (ended::timestamp - started::timestamp))::integer/60) AS TiempoSes, auth_user.username FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id WHERE auth_user.username = "+ uu+ "GROUP BY auth_user.username;"
        myQuery2="SELECT avg(extract (epoch from (ended::timestamp - started::timestamp))::integer/60) AS TiempoProm, auth_user.username FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id WHERE auth_user.username = "+ uu+ "GROUP BY auth_user.username;"
        myQuery3="SELECT min(extract (epoch from (ended::timestamp - started::timestamp))::integer/60) AS TiempoMin, auth_user.username FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id WHERE auth_user.username = "+ uu+ "GROUP BY auth_user.username;"
        myQuery4="SELECT max(extract (epoch from (ended::timestamp - started::timestamp))::integer/60) AS TiempoMax, auth_user.username FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id WHERE auth_user.username = "+ uu+ "GROUP BY auth_user.username;"
        myQuery5="SELECT max(day_number), auth_user.username FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id WHERE auth_user.username = "+ uu+ "GROUP BY auth_user.username;"

        #promedio exito fallo por nivel
        myQuery6="SELECT day_number, avg(success::int) FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id WHERE auth_user.username = "+ uu+ "GROUP BY day_number ORDER BY day_number;"

        #tiempo jugado vs compuestos hechos
        #myQuery7="SELECT extract (epoch from (ended::timestamp - started::timestamp))::integer/60 AS TiempoSesion, SUM(num_compounds_made) FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id WHERE auth_user.username = "+ uu+ "GROUP BY \"WEB_try\".session_id_id;"

        #myQuery7="SELECT extract (epoch from (ended::timestamp - started::timestamp))::integer/60 AS TiempoSesion, SUM(num_compounds_made) AS SumaCompuestos FROM \"WEB_day\" INNER JOIN \"WEB_try\" ON \"WEB_day\".try_id_id=\"WEB_try\".id INNER JOIN \"WEB_sesion\" ON \"WEB_try\".session_id_id= \"WEB_sesion\".id INNER JOIN \"WEB_usuario\" ON \"WEB_sesion\".user_id_id= \"WEB_usuario\".id INNER JOIN auth_user ON \"WEB_usuario\".id = auth_user.id WHERE auth_user.username = "+ uu+ " GROUP BY \"WEB_sesion\".ended, \"WEB_sesion\".started ORDER BY TiempoSesion ASC;"
        myQuery7="SELECT extract (epoch from (ended::timestamp - started::timestamp))::integer/60 AS TiempoSesion, SUM(num_compounds_made) AS SumaCompuestos FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id WHERE auth_user.username = "+ uu+ "GROUP BY \"WEB_sesion\".id;"
        #myQuery8="SELECT SUM(num_compounds_made) FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id WHERE auth_user.username = "+ uu+ "GROUP BY \"WEB_sesion\".id;"

        myQuery8="SELECT ended::timestamp, started::timestamp FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id WHERE auth_user.username = "+ uu+ ";"
        #Compuestos vendidos vs Elementos Comprados
        myQuery9="SELECT num_compounds_sold, num_elements_purchased FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id WHERE auth_user.username = "+ uu+ ";"

        myQuery10 ="SELECT day_number, AVG(num_compounds_sold) AS PromCompuestosVendidos, AVG(num_elements_purchased) AS PromElementos, AVG(customers_rejected) AS PromClientesRechazados FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id WHERE auth_user.username = "+ uu+ " GROUP BY day_number;"

        #inidicadores por nivel, Nivel vs (compuestos, elementos, clientes)


        #SELECT ''''' FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id
        cursor.execute(myQuery)
        cursor2.execute(myQuery2)
        cursor3.execute(myQuery3)
        cursor4.execute(myQuery4)
        cursor5.execute(myQuery5)
        cursor6.execute(myQuery6)
        cursor7.execute(myQuery7)
        cursor8.execute(myQuery8)
        cursor9.execute(myQuery9)
        cursor10.execute(myQuery10)

        rows = cursor.fetchall()
        rows2 = cursor2.fetchall()
        rows3 = cursor3.fetchall()
        rows4 = cursor4.fetchall()
        rows5 = cursor5.fetchall()
        rows6 = cursor6.fetchall()
        rows7 = cursor7.fetchall()
        rows8 = cursor8.fetchall()
        rows9 = cursor9.fetchall()
        rows10 = cursor10.fetchall()

        dat8=[]
        for tt in rows8:
            data8.append([tt[0]])
            dat8.append([tt[1]])

        finSes= np.max(data8)- timedelta(hours=5)

        print(finSes)
        inicioSes= np.max(dat8)- timedelta(hours=5)
        print(inicioSes)

        if len(rows6)>0:
            for rowq in rows6:
                data6.append([rowq[0], int(rowq[1]*100)])
            data6_formato = dumps(data6)
        else:
            return render(request, 'sinRegistros.html', {'nombre':uuu})
            '''
        ota= []
        ota2=[]
        for row in rows7:
            ota.append(row[0])
        for rowe in rows8:
            ota2.append(rowe[0])

        for i in range(len(ota)):
            data7.append([ota[i], ota2[i]])
        data7_formato= dumps(data7)
        '''
        for ee in rows7:
            data7.append([ee[0],ee[1]])
        data7_formato = dumps(data7)

        for roww in rows9:
            data9.append([roww[0], roww[1]])
        data9_formato = dumps(data9)

        for rowww in rows10:
            data10.append([rowww[0], int(rowww[1]), int(rowww[2]/10), int(rowww[3])])
        data10_formato = dumps(data10)

    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    finally:
        if(connection != None):
            cursor.close()
            connection.close()

    return render(request, 'mi_estadistica.html', {'nombre':uuu,'tiempoTot':rows[0][0], 'tiempoProm':str(round(rows2[0][0], 2)), 'tiempoMin':rows3[0][0], 'tiempoMax':rows4[0][0], 'nivelMax':rows5[0][0],'datos6':data6_formato, 'datos7':data7_formato, 'datos9':data9_formato, 'datos10':data10_formato, 'finSes':finSes, 'inicioSes':inicioSes})


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
        print(360)
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
        print(373)
        connection = psycopg2.connect(
            user = "farmaceuticouser",
            password = "LibroVerde23",
            host = "localhost",
            port = "5432",
            database = "medchembd"
        )

        data8= []
        data3 =[]
        data4= []
        data5=[]
        data6 = []
        data7= []
        data8.append(['Tiempo', 'Compuestos hechos'])
        data3.append(['Nivel','Compuestos','Elementos', 'Clientes'])
        data4.append(['Edad', 'Tiempo'])
        data5.append(['Dia ', 'Exito'])
        data7.append(['Genero','Numero'])
        print(393)

        cursor8 = connection.cursor()
        cursor3 = connection.cursor()
        cursor4 = connection.cursor()
        cursor5 = connection.cursor()
        cursor6 = connection.cursor()
        cursor7 = connection.cursor()


        #Tiempo jugado vs compuestos hechos
        cursor8.execute("SELECT extract (epoch from (ended::timestamp - started::timestamp))::integer/60 AS TiempoSesion, SUM(num_compounds_made) AS SumaCompuestos FROM \"WEB_day\" INNER JOIN \"WEB_try\" ON \"WEB_day\".try_id_id=\"WEB_try\".id INNER JOIN \"WEB_sesion\" ON \"WEB_try\".session_id_id= \"WEB_sesion\".id INNER JOIN \"WEB_usuario\" ON \"WEB_sesion\".user_id_id= \"WEB_usuario\".id INNER JOIN auth_user ON \"WEB_usuario\".id = auth_user.id GROUP BY \"WEB_sesion\".ended, \"WEB_sesion\".started ORDER BY TiempoSesion ASC;")

        #Nivel vs (compuestos, elementos, clientes, dinero)
        #la gigante
        cursor3.execute("SELECT day_number, AVG(num_compounds_sold) AS PromCompuestosVendidos, AVG(num_elements_purchased) AS PromElementos, AVG(customers_rejected) AS PromClientesRechazados FROM \"WEB_day\" GROUP BY day_number;") #

        #Edad vs tiempo jugado
        cursor4.execute("SELECT  DATE_PART('year', CURRENT_DATE::date) - DATE_PART('year', birthdate::date) AS Edad, avg(extract (epoch from (ended::timestamp - started::timestamp))::integer/60) AS Tiempo FROM \"WEB_sesion\" INNER JOIN \"WEB_usuario\" ON \"WEB_sesion\".user_id_id=\"WEB_usuario\".id GROUP BY Edad ;") #

        #Promedio de éxito / fallo por nivel
        cursor5.execute("SELECT day_number, avg(success::int) AS PromedioExito FROM \"WEB_day\" GROUP BY day_number ORDER BY day_number;")

        #Top five de scores
        cursor6.execute("SELECT auth_user.username, (AVG(money_generated_day)*MAX(day_number)) AS Score FROM auth_user INNER JOIN \"WEB_usuario\" ON auth_user.id= \"WEB_usuario\".username_id INNER JOIN \"WEB_sesion\" ON \"WEB_usuario\".id =\"WEB_sesion\".user_id_id INNER JOIN \"WEB_try\" ON \"WEB_try\".session_id_id = \"WEB_sesion\".id INNER JOIN \"WEB_day\" ON \"WEB_try\".id =\"WEB_day\".try_id_id GROUP BY username ORDER BY Score DESC LIMIT 5 ;")

        #genero
        cursor7.execute("SELECT gender, count(id)  FROM \"WEB_usuario\" GROUP BY gender;")

        rows8= cursor8.fetchall()
        rows3= cursor3.fetchall()
        rows4= cursor4.fetchall()
        rows5= cursor5.fetchall()
        rows6= cursor6.fetchall()
        rows7= cursor7.fetchall()

        for roweee in rows3:
            data3.append([int(roweee[0]), int(roweee[1]), int(roweee[2])/10, int(roweee[3])])

        data3_formato = dumps(data3)

        for rowee in rows4:
            data4.append([int(rowee[0]), int(rowee[1])])
        data4_formato = dumps(data4)

        for rowa in rows5:
            data5.append([rowa[0], int(rowa[1]*100)])
        data5_formato = dumps(data5)

        contador = 1
        for roowe in rows6:
            data6.append([contador, roowe[0], int(roowe[1]) ])
            contador = contador+1
        data6_formato= dumps(data6)
        print(data6[0][1])


        for rowaa in rows7:
            data7.append([rowaa[0],rowaa[1]])
        data7_formato= dumps(data7)

        for rowaar in rows8:
            data8.append([rowaar[0],rowaar[1]])
        data8_formato= dumps(data8)



        #'losDatos2':data2_formato, 'losDatos4':data4_formato, 'losDatos3':data3_formato, 'losDatos5':data5_formato, 'losDatos6':data6_formato, 'losDatos7':data7_formato, 'minutosTotales':str(round(minutosTotales, 2)) ,'promTemp':str(round(promTemp, 2)), 'maxTiempo':str(round(maxTiempo, 2)), 'minTiempo':str(round(minTiempo, 2))}
        elJson = {'losDatos':data_formato}

    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is now closed")

    return render(request, 'estadistica.html', {'losDatos':data8_formato, 'losDatos2':data2_formato, 'losDatos4':data4_formato, 'losDatos3':data3_formato, 'losDatos5':data5_formato, 'losDatos6':data6_formato, 'losDatos7':data7_formato, 'minutosTotales':str(round(minutosTotales, 2)) ,'promTemp':str(round(promTemp, 2)), 'maxTiempo':str(round(maxTiempo, 2)), 'minTiempo':str(round(minTiempo, 2))});
