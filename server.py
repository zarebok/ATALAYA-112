# -*- coding: utf-8 -*-
#!/usr/bin/python

import pg
import time
import openrouteservice
from openrouteservice import convert
import json

# Creamos la conexión
conexion = pg.DB(host="192.168.1.250", user="jesus2020", passwd="jesus2020", dbname="jesus2020")

coords = ((-3.635017,40.540277),(-3.620484,40.534947))
client = openrouteservice.Client(key='5b3ce3597851110001cf6248f2ed7abeb83047e6a74f5b73c4d2758d') # Specify your personal API key
geometry = client.directions(coords)['routes'][0]['geometry']

decoded = convert.decode_polyline(geometry)
# Ejecutamos una consulta y guaramos los resultados
x = -3.620484;
y = 40.534947;
dire = 0;
for i in decoded['coordinates']:
	print i
	x = i[0];
	y = i[1];
	dire += 10;
	if dire>=360: 
		dire = 0; 
	print("x es: " +str(x) + "  Y es:" +str(y)+ " DIRE ES: " + str(dire))		
	resultados = conexion.query("update lugares SET geom = ST_GeomFromText('POINT("+str(x)+" "+str(y)+")',4326), direccion = "+str(dire)+" WHERE ID = 8;")
	time.sleep(0.5)
print("Programa terminado")



# Recorremos los resultados y los mostramos
#for name, color in resultados.getresult() :
#    print name, color

# Cerramos la conexión
conexion.close()