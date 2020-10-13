# -*- coding: utf-8 -*-
#!/usr/bin/python

import pg

# Creamos la conexión
conexion = pg.DB(host="192.168.1.250", user="jesus2020", passwd="jesus2020", dbname="jesus2020")

# Ejecutamos una consulta y guaramos los resultados
resultados = conexion.query("SELECT name, color FROM lugares")

# Recorremos los resultados y los mostramos
for name, color in resultados.getresult() :
    print name, color

# Cerramos la conexión
conexion.close()