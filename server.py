#!/usr/bin/python
# encoding: utf-8

import pg
import time
import openrouteservice
from openrouteservice import convert
import json
import threading
import os
import random
from flask import Flask
from flask import request
from flask_cors import CORS
from waitress import serve
from datetime import datetime
#from flask_sslify import SSLify
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.load_cert_chain('/etc/letsencrypt/live/zarbok.ddns.net/cert.pem', '/etc/letsencrypt/live/zarbok.ddns.net/privkey.pem')

app = Flask(__name__)
#sslify = SSLify(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r"/*": {"origins": "*"}})
# Creamos la conexión al POSTGRES
conexion = pg.DB(host="192.168.1.250", user="jesus2020", passwd="jesus2020", dbname="jesus2020")
# Creamos la conexion al servicio de rutas
client = openrouteservice.Client(key='5b3ce3597851110001cf6248f2ed7abeb83047e6a74f5b73c4d2758d') # Specify your personal API key
tareabbdd = ''

def current_date_format():
    now = datetime.now()
    format = now.strftime('%Y-%m-%d %H:%M:%S')
    print(format)

    return format
    
def addtarea(tarea):
    global tareabbdd
    tareabbdd += str(tarea);    
  
def damesiguiente():
    global conexion
    while True:
        try:
            resultados = conexion.query("select * from test_id_seq;")  
            print(resultados.getresult())
            for last_value in resultados.getresult() :
                return int(last_value[1])
        except:
            print("FALLO CONSULTANDO VALOR ACTUAL EN BBDD A LAS: " +str(datetime.now()))
            conexion.close()
            conexion = pg.DB(host="192.168.1.250", user="jesus2020", passwd="jesus2020", dbname="jesus2020")  

def grabatarea():
    global tareabbdd
    global conexion
    hilog = threading.Timer(1.5, grabatarea)
    hilog.setDaemon(True)
    hilog.start()
    if tareabbdd != '':
        try:
            #print(tareabbdd)
            resultados = conexion.query(tareabbdd)
            tareabbdd = ''
        except:
            print(tareabbdd)    
            print("FALLO en grabatarea() INGRESANDO EN BBDD A LAS: " +str(datetime.now()))
            conexion.close()
            conexion = pg.DB(host="192.168.1.250", user="jesus2020", passwd="jesus2020", dbname="jesus2020") 
    
   
class asigna_tarea_incidencia(object):
    def tarea(self, argument):
        """Dispatch method"""
        method_name = str(argument)  #argument debe ser el tipo de incidencia (robo, pelea, etc)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Incidencia invalida")
        # Call the method as we return it
        return method()
 
    def ladron(self):
        return [["policia","nadie"]]
 
    def incendio(self):
        return [["bombero","nadie"]]
 
    def herido(self):
        return [["policia","nadie"],["sanidad","nadie"]]

    def trafico(self):
        return [["policia","nadie"]]

    def terremoto(self):
        return [["policia","nadie"],["bombero","nadie"]]

    def pelea(self):
        return [["policia","nadie"],["sanidad","nadie"]]

    def vdg(self):
        return [["policia","nadie"],["sanidad","nadie"]]

    def virus(self):
        return [["policia","nadie"],["sanidad","nadie"],["bombero","nadie"]]        


def patrullar(self, decoded, contador, cometido, idpatrus):
    #global conexion
    threading.current_thread().name = self.name;
    threading.current_thread().id = self.id;
    if self.debemorir:
        try:#por si acaso nunca esta demas, al no ser que nececitamos aquellos pocos ciclos que ocupa
            thread.exit()
        except:
            print("Error al acabar el proceso hijo " + str(self.id))
    '''Mueve la patrulla hasta que acaba la lista de coordenadas'''
    nueva=False
    for i in decoded['coordinates']:
        #print i
        dire = 0            
        x = i[0];
        y = i[1];
        dire += 10;
        if dire>=360: 
            dire = 0; 
        #print("x es: " +str(x) + "  Y es:" +str(y)+ " DIRE ES: " + str(dire))        
        self.latitud = y
        self.longitud = x
        #print(self.name + " continua "+str(idpatrus)+" en cometido "+cometido+" hacia " + str(x) + " " +str(y))
        addtarea("update lugares SET geom = ST_GeomFromText('POINT("+str(x)+" "+str(y)+")',4326) WHERE id = '"+ str(self.id)+"';")
        time.sleep(0.5)
        if self.cometido!=cometido:
            print("CAMBIANDO EL COMETIDO: SELF.COMETIDO ES: "+ self.cometido + " Y COMETIDO ES: " + cometido)
            nueva=True
            break
    if cometido=="finservicio":
        self.elimina(idpatrus)          
    if (self.cometido=="patrullando" and nueva==False):
        long=round(random.uniform(-3.661257, -3.607165),6)
        lat=round(random.uniform(40.507342, 40.561603),6)
        print(self.name + " CAMBIA "+str(idpatrus)+" la PATRULLA hacia " + str(lat) + " " +str(long))
        self.ruta(lat, long, 0 , self.cometido, idpatrus)
    if (self.cometido=="tarea" and nueva==False):
        print(self.name + " ACTUANDO EN LA TAREA DURANTE "+str(contador))
        mensajes.append([len(mensajes),current_date_format(),"La patrulla "+self.name+" ha llegado a la incidencia asignada."])
        for i in range(contador):
            #print(self.name + " ACTUANDO CONTADOR"+str(i))
            time.sleep(1)
        for x in incidas:
            z=0
            for y in x.tarea:
                #print("y[1] es:"+str(y[1]) + " self.name "+ self.name)
                if(y[1]==self.name):
                    print(y[1] + " ha terminado con la tarea.")
                    mensajes.append([len(mensajes),current_date_format(),"La patrulla "+self.name+" ha terminado en la incidencia asignada. Regresando a patrullar."])
                    x.tarea.pop(z)
                    break
                z=z+1
        
        long=round(random.uniform(-3.661257, -3.607165),6)
        lat=round(random.uniform(40.507342, 40.561603),6)        
        print(self.name + " volviendo a patrullar "+str(idpatrus)+" la PATRULLA hacia " + str(lat) + " " +str(long))
        self.ruta(lat, long, 0 , "patrullando", idpatrus)        
        
    

    

        
        
class patrulla:
    rol = 'patrulla'     
    cometido = 'nada'       
    cuerpo = 'nacional' #nacional,local,bombero,sanidad
    debemorir = False
    id = 0
    name = ''
    latitud = 0
    longitud = 0
    contador = 0
    hilo = 0
    ruta = []
    def elimina(self,idpatrus):
        addtarea("DELETE FROM lugares WHERE name = '"+ str(self.name)+"';")            
        patrus.pop(idpatrus) 
        print("Eliminando patrulla con IDPATRUS:" +str(idpatrus) + " Y nombre: "+ self.name)
        mensajes.append([len(mensajes),current_date_format(),"Patrulla "+self.name+" ha terminado el servicio."]) 
        self.debemorir = True
        
    def ruta(self, lat, long, contador, cometido,idpatrus):
        self.contador = contador
        self.cometido = cometido
        coords = ((self.longitud,self.latitud),(long,lat))
        print(coords)
        geometry = client.directions(coords)['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)   
        self.contador = self.contador +1
        addtarea("update lugares SET cometido = '"+str(cometido)+"' WHERE id = '"+ str(self.id)+"';")    
        self.hilo = threading.Thread(target=patrullar, args=(self, decoded, self.contador, cometido, idpatrus), )
        self.hilo.start()     
        
    def __init__(self, id, name, lat, long, cometido, cuerpo, nueva):
        self.id = id    # instance variable unique to each instance
        self.name = name    # instance variable unique to each instance        
        self.latitud = lat
        self.longitud = long
        self.cometido = cometido
        longrand=round(random.uniform(-3.661257, -3.607165),6)
        latrand=round(random.uniform(40.507342, 40.561603),6)
        coords = ((self.longitud,self.latitud),(longrand, latrand))
        decoded = []
        try:
            geometry = client.directions(coords)['routes'][0]['geometry']
            decoded = convert.decode_polyline(geometry)    
        except:
            print(str(name)+" FALLO EL GEOMETRY")
        if nueva == True:
            addtarea("INSERT INTO lugares (geom, name, cuerpo, tipo, direccion, cometido) VALUES (ST_GeomFromText('POINT("+str(long)+" "+str(lat)+")',4326),'" + str(name)+"', '"+str(cuerpo)+"', '"+str(self.rol)+"', 0, '"+str(cometido)+"');")    
        self.contador = self.contador +1
        mensajes.append([len(mensajes),current_date_format(),"Patrulla "+self.name+" ha iniciado el servicio."]) 
        self.hilo = threading.Thread(target=patrullar, args=(self, decoded, self.contador, cometido, 0))
        self.hilo.setDaemon(True)
        self.hilo.start()
        
def incide(self, ):
    #global conexion
    global patrus
    threading.current_thread().name = self.name;
    threading.current_thread().id = self.id;
    if self.debemorir:
        try:#por si acaso nunca esta demas, al no ser que nececitamos aquellos pocos ciclos que ocupa
            thread.exit()
        except:
            print("Error al acabar el proceso hijo " + str(self.id))
    '''GESTIONAR INCIDENCIA'''
    while True:
        #print("INCIDAS ESTA FUNCIONANDO")
        if(len(self.tarea)==0):
            z=0
            for x in incidas:
                if(x.name==self.name):
                    incidas[z].elimina(z)
                    print("LA INCIDENCIA SE HA QUEDADO SIN TAREAS. ELIMINANDO INCIDENCIA")
                    mensajes.append([len(mensajes),current_date_format(),"La incidencia "+self.name+" ha sido resuelta. Cerrando incidencia."])
                    break
                z=z+1                        
                    
        time.sleep(1) #incidencias se actualizan cada segundo
    '''FIN GESTIONAR INCIDENCIA'''
    

        
class incidencia:
    rol = 'incidencia'         
    cometido = 'nada'         
    cuerpo = 'ladron'   #ladron,incendio,herido,trafico,
    debemorir = False
    tarea = []
    id = 0
    name = ''
    latitud = 0
    longitud = 0
    contador = 0
    ruta = []
    def elimina(self, idincidas):
        addtarea("DELETE FROM lugares WHERE name = '"+ str(self.name)+"';")            
        incidas.pop(idincidas) 
        self.debemorir = True
        
    def dame_tarea(self):
        return self.tarea

    def cambia_tarea(self,tarea,resul):
        for x in range(len(self.tarea)):
            if(self.tarea[x][0]==tarea):
                self.tarea[x][1]=resul
                #self.hilo = threading.Thread(target=incide, args=(self, resul, random.randrange(0, 101, 2),))
                #self.hilo.setDaemon(True)
                #self.hilo.start()
                print("TAREA "+self.name+" CAMBIA SU TAREA " + tarea + " POR " + resul)                
    
        
    def __init__(self, id, name, lat, long, cometido, cuerpo, nueva):
        self.id = id    # instance variable unique to each instance
        self.name = name    # instance variable unique to each instance        
        self.latitud = lat
        self.longitud = long
        self.cometido = cometido

        #METE LAS TAREAS AQUIIIIIIIIIIIIIIIIIIIIIII  
        a=asigna_tarea_incidencia()
        self.tarea=a.tarea(cuerpo)     
        print("LA TAREA con ID "+str(self.id)+" ES:" + str(self.tarea) + "y cometido es:" + str(cuerpo))      
        if nueva == True:
            addtarea("INSERT INTO lugares (geom, name, cuerpo, tipo, direccion, cometido) VALUES (ST_GeomFromText('POINT("+str(long)+" "+str(lat)+")',4326),'" + str(name)+"', '"+str(cuerpo)+"', '"+str(self.rol)+"', 0, '"+str(cometido)+"');")    
        mensajes.append([len(mensajes),current_date_format(),"Nueva incidencia "+self.name+" creada."])
        self.hilo = threading.Thread(target=incide, args=(self,))
        self.hilo.setDaemon(True)
        self.hilo.start()
        

patrus = []
incidas = []
mensajes = []

resultados = conexion.query("SELECT *,ST_X(geom),ST_Y(geom) FROM lugares WHERE TIPO = 'patrulla' OR  TIPO = 'incidencia' ORDER BY id ASC ")
if not resultados.getresult():
    try:
        addtarea("INSERT INTO lugares (geom, name, cuerpo, tipo, direccion, cometido) VALUES (ST_GeomFromText('POINT(-3.623254 40.547912)',4326),'415-A', 'nacional', 'patrulla', 0, 'patrullando');")
        grabatarea()
        resultados = conexion.query("SELECT *,ST_X(geom),ST_Y(geom) FROM lugares WHERE TIPO = 'patrulla' ORDER BY id ASC ")
    except:
        print("FALLO INGRESANDO EN BBDD LA PRIMERA CONSULTA")        
for id, name, geom, cuerpo, tipo, direccion, cometido, st_x, st_y in resultados.getresult() :
    if(cuerpo=="nacional" or cuerpo=="local" or cuerpo=="bombero" or cuerpo=="sanidad"):
        print("ID DE PRIMERA CREACIÓN ES: " + str(id))
        patrus.append(patrulla(id,name,st_y,st_x,cometido,cuerpo,False))       
    else:
        incidas.append(incidencia(id,name,st_y,st_x,cometido,cuerpo,False))



grabatarea()

@app.route("/")
def hello():
    texto = "Elige opción:<form action='./resultado' method='post'>"
    texto += "<p><select name='opcion' size='9'>"
    texto += "<option value='1'>Ver patrullas</option>"
    texto += "<option value='2'>Añadir patrulla</option>"
    texto += "<option value='3'>Enviar patrulla</option>"
    texto += "<option value='4'>Eliminar patrulla</option>"
    texto += "<option value='5'>Ver incidencias</option>"    
    texto += "<option value='6'>Añadir incidencia</option>"
    texto += "<option value='7'>Modificar incidencia (PENDIENTE)</option>"
    texto += "<option value='8'>Eliminar incidencia</option>"    
    texto += "<option value='damemensajes'>Dame mensajes</option>"       
    texto += "</select></p><p><input type='submit' value='Enviar'></p>"
    return texto

@app.route('/resultado',methods=['POST'])
def formulario():
    texto = ""
    try:
        opcionMenu = request.form['opcion']
    except:
        return render_template('./')
    if opcionMenu=="1":
        texto += "Las patrullas actuales son: <br>"
        x=0
        for i in patrus:
            texto += str(x) + " Con identificador: " +str(i.id) + "  Nombre:" +str(i.name)+ " De tipo "+str(i.cuerpo)+" Actualmente esta en: " + str(i.latitud) + " " + str(i.longitud) + " Con el cometido: " + str(i.cometido)
            if i.hilo.is_alive():
               texto += " Y su hilo esta vivo<br>"
            else:
               texto += " Y su hilo esta muerto<br>"
            x+=1
        texto += "<br><a href='./'>Volver al indice</a>"
        
    elif opcionMenu=="2":
        texto += "<form action='./resultado' method='post'>Insertando patrulla:<br><br><br><input type='hidden' id='opcion' value='22' name='opcion'>"
        texto += "Inserta un nombre:<br>"
        texto += "<input type='text' id='opcionname' name='opcionname'><br><br>"
        texto += "Inserta un cuerpo (nacional,local,bombero,sanidad):<br>"
        texto += "<select name='opcioncuerpo' size='4'><option value='nacional'>Policia nacional</option><option value='local'>Policia local</option><option value='bombero'>Bomberos</option><option value='sanidad'>Ambulancia</option></select><br><br>"
        texto += "Inserta una latitud (entre 40.507342 y 40.561603) o inserte 'a' para aleatorio:<br>"
        texto += "<input type='text' id='opcionlat' name='opcionlat'><br><br>"
        texto += "Inserta una longitud (entre -3.607165 y -3.661257) o inserte 'a' para aleatorio:<br>"
        texto += "<input type='text' id='opcionlong' name='opcionlong'><br><br>"        
        texto += "Inserta un cometido:<br>"
        texto += "<input type='text' id='opcioncometido' name='opcioncometido'><br><br><p><input type='submit' value='Enviar'></p></form><a href='./'>Volver al indice</a>"   
        
    elif opcionMenu=="22":   
        try:
            opcionname = request.form['opcionname']
            opcioncuerpo = request.form['opcioncuerpo']
            opcionlat = request.form['opcionlat']
            opcionlong = request.form['opcionlong']
            opcioncometido = request.form['opcioncometido']           
        except:
            return render_template('./resultado?opcion=2')        
        if opcionlat == 'a':
            opcionlat=round(random.uniform(40.507342, 40.561603),6)
        if float(opcionlat) < 40.507342:
            texto += "Latitud menor que 40.507342, seleccionando 40.507342.<br>"
            opcionlat = 40.507342
        if float(opcionlat) > 40.561603:
            texto += "Latitud mayor que 40.561603, seleccionando 40.561603.<br>"
            opcionlat = 40.561603   
        if opcionlong == 'a':
            opcionlong=round(random.uniform(-3.661257, -3.607165),6)        
        if float(opcionlong) < -3.661257:
            texto += "Latitud menor que -3.661257, seleccionando -3.661257.<br>"
            opcionlong = -3.661257
        if float(opcionlong) > -3.607165:
            texto += "Latitud mayor que -3.607165, seleccionando -3.607165.<br>"
            opcionlong = -3.607165  
        
        q=damesiguiente()
        patrus.append(patrulla((q+1), opcionname, float(opcionlat), float(opcionlong), opcioncometido, opcioncuerpo, True))
        texto += "Patrulla creada.<br><a href='./'>Volver al indice</a>"
        print("Patrulla "+opcionname+" del "+opcioncuerpo+" creada.")
        
    elif opcionMenu=="3":
        texto += "Las patrullas disponibles son: <br>"
        iden="";
        x=0;
        for i in patrus:
            texto += str(x) + " Con identificador: " +str(i.id) + "  Nombre:" +str(i.name)+ " De tipo "+str(i.cuerpo)+" Actualmente esta en: " + str(i.latitud) + " " + str(i.longitud) + " Con el cometido: " + str(i.cometido) + "<br>"    
            iden+="<option value='" +str(x) + "'>" +str(x) +" "+str(i.name)+ "</option>"
            x+=1
        texto += "<br><form action='./resultado' method='post'>Insertando patrulla:<br><br><br><input type='hidden' id='opcion' value='33' name='opcion'>"
        texto += "Elige un nombre:<br>"
        texto += "<select name='opcionid' size='"+str(x)+"'>"+str(iden)+"</select><br><br>"
        texto += "Inserta una latitud (entre 40.507342 y 40.561603) o inserte 'a' para aleatorio:<br>"
        texto += "<input type='text' id='opcionlat' name='opcionlat'><br><br>"
        texto += "Inserta una longitud (entre -3.607165 y -3.661257) o inserte 'a' para aleatorio:<br>"
        texto += "<input type='text' id='opcionlong' name='opcionlong'><br><br>"        
        texto += "Inserta un cometido:<br>"
        texto += "<input type='text' id='opcioncometido' name='opcioncometido'><br><br><p><input type='submit' value='Enviar'></p></form><a href='./'>Volver al indice</a>"  
        
    elif opcionMenu=="33":    
        try:
            opcionid = request.form['opcionid']
            opcionlat = request.form['opcionlat']
            opcionlong = request.form['opcionlong']
            opcioncometido = request.form['opcioncometido']            
        except:
            return render_template('./resultado?opcion=3')        
        if opcionlat == 'a':
            opcionlat=round(random.uniform(40.507342, 40.561603),6)
        if float(opcionlat) < 40.507342:
            texto += "Latitud menor que 40.507342, seleccionando 40.507342.<br>"
            opcionlat = 40.507342
        if float(opcionlat) > 40.561603:
            texto += "Latitud mayor que 40.561603, seleccionando 40.561603.<br>"
            opcionlat = 40.561603   
        if opcionlong == 'a':
            opcionlong=round(random.uniform(-3.661257, -3.607165),6)        
        if float(opcionlong) < -3.661257:
            texto += "Latitud menor que -3.661257, seleccionando -3.661257.<br>"
            opcionlong = -3.661257
        if float(opcionlong) > -3.607165:
            texto += "Latitud mayor que -3.607165, seleccionando -3.607165.<br>"
            opcionlong = -3.607165           
        patrus[int(opcionid)].ruta(float(opcionlat), float(opcionlong), 0 ,opcioncometido,opcionid)  
        texto += "Patrulla enviada a "+opcioncometido+".<br><a href='./'>Volver al indice</a>" 
        print("Patrulla "+opcionid+" enviada a "+opcioncometido+".")
        
    elif opcionMenu=="4":
        texto += "Las patrullas disponibles son: <br>"
        iden="";
        x=0;
        for i in patrus:
            texto += str(x) + " Con identificador: " +str(i.id) + "  Nombre:" +str(i.name)+ " De tipo "+str(i.cuerpo)+" Actualmente esta en: " + str(i.latitud) + " " + str(i.longitud) + " Con el cometido: " + str(i.cometido) + "<br>"    
            iden+="<option value='" +str(x) + "'>" +str(x) +" "+str(i.name)+ "</option>"
            x+=1
        texto += "<br><form action='./resultado' method='post'>Insertando patrulla:<br><br><br><input type='hidden' id='opcion' value='44' name='opcion'>"
        texto += "Elige una patrulla para eliminar:<br>"
        texto += "<select name='opcionpatrus' size='"+str(x)+"'>"+str(iden)+"</select><br><br>"
        texto += "<p><input type='submit' value='Enviar'></p></form><br><a href='./'>Volver al indice</a>"
        
    elif opcionMenu=="44":        
        opcionpatrus = request.form['opcionpatrus']   
        patrus[int(opcionpatrus)].elimina(int(opcionpatrus))        
        texto +="</form>Patrulla eliminada...<a href='./'>Volver al indice</a>"
        print("Patrulla "+opcionpatrus+" eliminada.")

    elif opcionMenu=="finservicio":        
        opcionname = request.form['opcionname']   
        opcioncuerpo = request.form['opcioncuerpo'] 
        opcionid = request.form['opcionid'] 
                
        global conexion
        try:
            resultados = conexion.query("SELECT p1.id,p2.name,p2.geom,ST_X(p2.geom),ST_Y(p2.geom),ST_DistanceSphere(p1.geom,p2.geom) FROM lugares AS p1, lugares AS p2 WHERE p1.id > p2.id AND p1.id='"+opcionid+"' AND p2.cuerpo='"+opcioncuerpo+"' AND p2.tipo='base' ORDER BY ST_DistanceSphere(p1.geom,p2.geom);")  #realizo una consulta espacial a la base de datos buscando la base más cercana
        except:
            print("FALLO en finservicio INGRESANDO EN BBDD A LAS: " +str(datetime.now()))
            print(tareabbdd)
            conexion.close()
            conexion = pg.DB(host="192.168.1.250", user="jesus2020", passwd="jesus2020", dbname="jesus2020")
        #print(resultados)
        for id, name, geom, st_x, st_y, st_distancesphere in resultados.getresult() :
            x=0        
            for i in patrus:
                if(int(opcionid)==i.id):
                    patrus[x].ruta(float(st_y), float(st_x), 0 ,'finservicio',x)     
                    texto +="</form>Enviando a Fin de servicio la patrulla: "+opcionname+".<br><a href='./'>Volver al indice</a>"
                                       
                    #print("Enviando a Fin de servicio la patrulla: "+opcionname+".")        
                    #print("LAT: "+str(st_y)+".")
                    #print("LNG: "+str(st_x)+".")
                    break
                x=x+1

        
        '''INCIDENCIAS'''
    elif opcionMenu=="5":
        texto += "Las incidencias actuales son: <br>"
        x=0
        for i in incidas:
            texto += str(x) + " Con identificador: " +str(i.id) + "  Nombre:" +str(i.name)+ " De tipo "+str(i.cuerpo)+" Actualmente esta en: " + str(i.latitud) + " " + str(i.longitud) + " Con el cometido: " + str(i.cometido)
            if i.hilo.is_alive():
               texto += " Y su hilo esta vivo<br>"
            else:
               texto += " Y su hilo esta muerto<br>"
            x=x+1
        texto += "<br><a href='./'>Volver al indice</a>"      
        
    elif opcionMenu=="6":
        texto += "<form action='./resultado' method='post'>Insertando incidencia:<br><br><br><input type='hidden' id='opcion' value='66' name='opcion'>"
        texto += "Inserta un nombre:<br>"
        texto += "<input type='text' id='opcionname' name='opcionname'><br><br>"
        texto += "Inserta un tipo:<br>"
        texto += "<select name='opcioncuerpo' size='4'>"
        texto += "<option value='ladron'>Robo</option>"
        texto += "<option value='incendio'>Incendio</option>"
        texto += "<option value='herido'>Herido</option>"
        texto += "<option value='trafico'>Tráfico</option>"
        texto += "<option value='terremoto'>Terremoto</option>"
        texto += "<option value='pelea'>Pelea</option>"
        texto += "<option value='vdg'>Violencia de genero</option>"
        texto += "<option value='virus'>Virus</option>"
        texto += "</select><br><br>"
        texto += "Inserta una latitud (entre 40.507342 y 40.561603) o inserte 'a' para aleatorio:<br>"
        texto += "<input type='text' id='opcionlat' name='opcionlat'><br><br>"
        texto += "Inserta una longitud (entre -3.607165 y -3.661257) o inserte 'a' para aleatorio:<br>"
        texto += "<input type='text' id='opcionlong' name='opcionlong'><br><br>"        
        texto += "Inserta una descripción:<br>"
        texto += "<input type='text' id='opcioncometido' name='opcioncometido'><br><br><p><input type='submit' value='Enviar'></p></form><a href='./'>Volver al indice</a>" 
        
    elif opcionMenu=="66":    
        try:
            opcionname = request.form['opcionname']
            opcioncuerpo = request.form['opcioncuerpo']
            opcionlat = request.form['opcionlat']
            opcionlong = request.form['opcionlong']
            opcioncometido = request.form['opcioncometido']            
        except:
            return render_template('./resultado?opcion=6')        
        if opcionlat == 'a':
            opcionlat=round(random.uniform(40.507342, 40.561603),6)
        if float(opcionlat) < 40.507342:
            texto += "Latitud menor que 40.507342, seleccionando 40.507342.<br>"
            opcionlat = 40.507342
        if float(opcionlat) > 40.561603:
            texto += "Latitud mayor que 40.561603, seleccionando 40.561603.<br>"
            opcionlat = 40.561603   
        if opcionlong == 'a':
            opcionlong=round(random.uniform(-3.661257, -3.607165),6)        
        if float(opcionlong) < -3.661257:
            texto += "Latitud menor que -3.661257, seleccionando -3.661257.<br>"
            opcionlong = -3.661257
        if float(opcionlong) > -3.607165:
            texto += "Latitud mayor que -3.607165, seleccionando -3.607165.<br>"
            opcionlong = -3.607165
        q=damesiguiente()
        incidas.append(incidencia((q+1), opcionname, float(opcionlat), float(opcionlong), opcioncometido.encode('utf-8'), opcioncuerpo, True))
        texto += "Incidencia creada.<br><a href='./'>Volver al indice</a>" 
        print("Incidencia "+opcionname+" del tipo "+opcioncuerpo+" creada.")
        
    elif opcionMenu=="8":
        texto += "Las incidencias disponibles son: <br>"
        iden="";
        x=0;
        for i in incidas:
            texto += str(x) + "Con identificador: " +str(i.id) + "  Nombre:" +str(i.name)+ " De tipo "+str(i.cuerpo)+" Actualmente esta en: " + str(i.latitud) + " " + str(i.longitud) + " Con el cometido: " + str(i.cometido) + "<br>"    
            iden+="<option value='" +str(x) + "'>" +str(x) +" "+str(i.name)+ "</option>"
            x+=1
        texto += "<br><form action='./resultado' method='post'>Eliminando incidencia:<br><br><br><input type='hidden' id='opcion' value='88' name='opcion'>"
        texto += "Selecciona una incidencia para eliminar:<br>"
        texto += "<select name='opcionpatrus' size='"+str(x)+"'>"+str(iden)+"</select><br><br>"
        texto += "<p><input type='submit' value='Enviar'></p></form><br><a href='./'>Volver al indice</a>"
        
    elif opcionMenu=="88":        
        opcionpatrus = request.form['opcionpatrus']   
        incidas[int(opcionpatrus)].elimina(int(opcionpatrus))        
        texto +="</form>Incidencia eliminada.<br><a href='./'>Volver al indice</a>"      
        print("Incidencia "+opcionpatrus+" eliminada.")    
        
    elif opcionMenu=="dame_tarea":  
        opcionid = request.form['opcionid']      
        for i in incidas:
            if(i.id==int(opcionid)): 
                texto +=str(i.dame_tarea())
                break

        print("Incidencia: dame_tarea() de "+opcionid+": " + texto)     
        
    #DAME PATRULLAS ACTUANTES POR ORDEN CERNANIA
    elif opcionMenu=="dame_patrullas":  
        #global conexion
        texto =  '['
        opcionid = request.form['opcionid'] 
        opciontipo = request.form['opciontipo'] 
        for i in incidas:
            #print("i.id es:"+str(i.id) + " opcionid"+ opcionid)
            if(int(i.id)==int(opcionid)):
                #texto +=str(i.dame_tarea())
                #print("i.id es:"+str(i.id) + " opcionid"+ opcionid)
                if(opciontipo=="policia" ):
                    where="(p2.cuerpo='nacional' OR p2.cuerpo='local')"
                else:
                    where="p2.cuerpo='"+str(opciontipo)+"'"
                busca="SELECT p1.id, p2.name, p2.id AS id2,p2.geom,ST_X(p2.geom),ST_Y(p2.geom),ST_DistanceSphere(p1.geom,p2.geom) FROM lugares AS p1, lugares AS p2 WHERE p1.id='"+str(i.id)+"' AND p2.tipo='patrulla' AND p2.cometido='patrullando' AND "+where+" ORDER BY ST_DistanceSphere(p1.geom,p2.geom);"
                #print(busca)
                try:
                    resultados = conexion.query(busca)  #realizo una consulta espacial a la base de datos buscando la base más cercana
                except:
                    print("FALLO en finservicio INGRESANDO EN BBDD A LAS: " +str(datetime.now()))
                    print(tareabbdd)
                    conexion.close()
                    conexion = pg.DB(host="192.168.1.250", user="jesus2020", passwd="jesus2020", dbname="jesus2020")
                    #print(resultados)
                    
                for id, name, id2, geom, st_x, st_y, st_distancesphere in resultados.getresult() :
                    #texto +="Patrulla es: "+str(name)+ " con id:" + str(id) + " a una distancia de: " + str(st_distancesphere) + "metros\n"
                    texto +=  '{ "id":'+str(id)+', "name":"'+str(name)+'", "id2":'+str(id2)+', "geom":"'+str(geom)+'", "st_x":"'+str(st_x)+'", "st_y":"'+str(st_y)+'", "st_distancesphere":"'+str(st_distancesphere)+'"},'

                texto = texto[:-1]                            
                texto +=  ']'                            
                break
 
        
        print("Incidencia: dame_patrullas() de "+opcionid+": " + texto)    
        #print(texto)
    #ENVIA PATRULLAS ACTUANTES A UNA INCIDENCIA
    elif opcionMenu=="enviapatrullas":  
        #global conexion
        opcionid = request.form['opcionid']     #ID INCIDENCIA   
        opcionid2 = request.form['opcionid2']      #ID PATRULLA 
        opciontipo = request.form['opciontipo']         
        for i in incidas:
            if(i.id==int(opcionid)):
                x=0;
                for y in patrus:
                    if(y.id==int(opcionid2)):
                        #print("LATITUD DE INCIDENCIA "+str(i.name)+" ES: "+str(i.latitud)+ " Y LONGITUD DE INCIDENCIA ES: "+str(i.longitud))
                        #print("LATITUD DE PATRULLA   "+str(y.name)+" ES: "+str(y.latitud)+ " Y LONGITUD DE PATRULLA   ES: "+str(y.longitud))
                        texto = "Incidencia: enviapatrullas() de patrulla "+y.name+" "+opcionid2+" a incidencia "+i.name+" "+opcionid+"."  
                        mensajes.append([len(mensajes),current_date_format(),"Enviada patrulla "+y.name+" a incidencia "+i.name+"."])
                        i.cambia_tarea(opciontipo,y.name)
                        patrus[int(x)].ruta(i.latitud, i.longitud, random.randrange(20,100) ,"tarea",x)
                        break
                    x=x+1;

 
        
        
        print(texto)

    #DEVUELVE LAS NOVEDADES DE LOS MENSAJES
    elif opcionMenu=="damemensajes":  
        #global conexion
        texto =  '['
        if "ultimo" in request.form:
            ultimo = int(request.form['ultimo']) #ULTIMO MENSAJE ENVIADO
        else: 
            ultimo=0
        x=0
        #print(mensajes)
        for i in mensajes:
            #print("X ES: "+str(x)+ " ULTIMO ES: "+str(ultimo))
            x=x+1;
            if(x>ultimo):
                #print(i)
                texto=texto+str(i)+','

        texto =  texto+']'
        #print(texto)
        
    else:
        texto += "No has pulsado ninguna opción correcta.<br><a href='./'>Volver al indice</a>"
    return texto
    
    
# This is important so that the server will run when the docker container has been started. 
# Host=0.0.0.0 needs to be provided to make the server publicly available.
if __name__ == "__main__":
    #serve(app,host='0.0.0.0', port=5430, url_scheme='https')
    #app.run(host='0.0.0.0',port=5430, ssl_context=context, debug=True)
    app.run(host='0.0.0.0',port=5430, ssl_context=context)

print("HA REINICIADO")
while True:
    opcionMenu=5


# Cerramos la conexión al POSTGRES
conexion.close()