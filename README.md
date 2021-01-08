# 112-Emergencias
 Proyecto que integra una Interfaz grafica y un servidor de emergecias desarrollado como TFG de DAW 2020-2021 por Jesús Bueno Jiménez

###  RECURSOS
TECNOLOGIAS A USAR:
- PYTHON
- HTML
- POSTGRES
- POSTGIS 
- JAVASCRIPT
- DOCKER

APLICACIONES A USAR:
- PGADMIN
- LEAFLET
- POSTGIS
- POSTGRES
- GEOSERVER


### PUERTOS DE RED USADOS
postgres:5432
geoserver:5431
www:80


### TUTORIAL
#INSTALAMOS DOCKER EN LA RASPBERRY
Descargamos Docker con el siguiente comando:
	curl -sSL https://get.docker.com | sh
Creamos el Grupo "docker":
	sudo groupadd docker
Añadimos el usuario "pi" al grupo "docker":	
	sudo usermod -aG docker pi

#CARGAMOS NOIP PARA CONFIGURAR LA CONEXIÓN DESDE FUERA DE NUESTRA RED
Instalamos con el siguiente comando y configuramos nuestra cuenta:
	docker run -ti -v "/home/pi/docker/noip:/usr/local/etc/" hypriot/rpi-noip noip2 -C
Posteriormente ejecutamos este comando para que siempre se ejecute automaticamente:
	docker run -ti --name=noip -v /home/pi/docker/noip:/usr/local/etc/ -e TZ=Europe/Madrid -d --restart=always hypriot/rpi-noip
	
	
#AÑADIR INSTALACION DE APACHE Y PHP
Instalamos en docker APACHE con PHP de DOCKERHUB:
docker run -dit --name apache -p 80:80 --link mysql:db --restart unless-stopped -v /home/pi/www:/var/www/html/ php:7.2-apache
Ejecutamos dentro del docker:
docker exec -it apache bash
apt update
apt-get install libpq-dev
docker-php-ext-install pgsql


#POSTGIS Y POSTGRES
Instalamos en docker un POSTGIS 2.3 y POSTGRES 9.6 de DOCKERHUB https://hub.docker.com/r/tobi312/rpi-postgresql-postgis/
	docker run --name "postgis" \
	-e TZ=Europe/Madrid \
	-p 5432:5432 \
	-v $HOME/docker/TFG/postgresql:/var/lib/postgresql \
	-e POSTGRES_USER=jesus2020 \
	-e POSTGRES_PASSWORD=jesus2020 \
	-e POSTGRES_DBNAME=daw2020 \
	-e POSTGRES_MULTIPLE_EXTENSIONS=postgis,hstore,postgis_topology \
	-d \
	--restart unless-stopped \
	-t tobi312/rpi-postgresql-postgis:latest
	
Entramos en el docker y ejecutamos:
	docker exec -it postgis bash
	apt update
	apt-get install postgresql-contrib
	exit
	docker restart postgis
	
Instalamos Pgadmin y conectamos a la BBDD. Vemos que esta correctamente instalada la extensión POSTGIS: 
	SELECT postgis_version();

Creamos la extensión para las contraseñas seguras.	
	CREATE EXTENSION chkpass;

Creamos una tabla de usuarios y lugares:
	CREATE TABLE usuario (login varchar(100), password chkpass, permiso varchar(2));
	CREATE TABLE lugares ( id int4 primary key, name varchar(50), geom geometry(POINT,4326), cuerpo varchar(50), tipo varchar(50), direccion integer, cometido varchar(50));

Añadimos usuario administrador.
	INSERT INTO usuario(login, "password", permiso) VALUES ('admin', '1234', '1');
	
Añadimos algunos lugares , como la Bases de Policias y de Bomberos.
	INSERT INTO lugares (id, geom, name, cuerpo, tipo, direccion, cometido) VALUES (1,ST_GeomFromText('POINT(-3.635533 40.547141)',4326),'Policia Nacional', 'nacional', 'base', 0, 0);
	INSERT INTO lugares (id, geom, name, cuerpo, tipo, direccion, cometido) VALUES (2,ST_GeomFromText('POINT(-3.635017 40.540277)',4326),'Policia Local, Sede Centro', 'local', 'base', 0, 0);
	INSERT INTO lugares (id, geom, name, cuerpo, tipo, direccion, cometido) VALUES (3,ST_GeomFromText('POINT(-3.642802 40.527693)',4326),'Policia Local, Sede Urbanizaciones', 'local', 'base', 0, 0);
	INSERT INTO lugares (id, geom, name, cuerpo, tipo, direccion, cometido) VALUES (4,ST_GeomFromText('POINT(-3.661999 40.547547)',4326),'Policia Local, Sede Norte', 'local', 'base', 0, 0);
	INSERT INTO lugares (id, geom, name, cuerpo, tipo, direccion, cometido) VALUES (5,ST_GeomFromText('POINT(-3.620484 40.534947)',4326),'Bomberos', 'bombero', 'base', 0, 0);
	INSERT INTO lugares (id, geom, name, cuerpo, tipo, direccion, cometido) VALUES (6,ST_GeomFromText('POINT(-3.620866 40.527777)',4326),'Hospital Clinico Alcobendas', 'sanidad', 'base', 0, 0);
	INSERT INTO lugares (id, geom, name, cuerpo, tipo, direccion, cometido) VALUES (7,ST_GeomFromText('POINT(-3.643254 40.547912)',4326),'Hospital La Paz Alcobendas', 'sanidad', 'base', 0, 0);


//UPDATE update lugares SET geom = ST_GeomFromText('POINT(-3.620484 40.534947)',4326) WHERE ID = 5;
//UPDATE update lugares SET geom = ST_GeomFromText('POINT(-3.635533 40.547141)',4326) WHERE ID = 5;
//UPDATE update lugares SET geom = ST_GeomFromText('POINT(-3.643254 40.547912)',4326) WHERE ID = 5;
Comprobamos que la inserción ha sido correcta:
	SELECT * FROM lugares;

Esto nos da capacidad de hacer consultas espaciales a la base de datos. Por ejemplo distancia entre puntos:
	SELECT p1.name,p2.name,ST_DistanceSphere(p1.geom,p2.geom) FROM lugares AS p1, lugares AS p2 WHERE p1.id > p2.id;
	

#GEOSERVER
Instalamos un GEOSERVER en docker. Como no existe uno para Raspberry (mi servidor) uso de DOCKERHUB https://hub.docker.com/r/arm32v7/tomcat/tags y con las siguientes instrucciones: https://github.com/thinkWhere/GeoServer-Docker
	docker run --name "geoserver" \
	-e TZ=Europe/Madrid \
	-p 5431:8080 \
	-v $HOME/docker/TFG/geoserver_tomcat:/usr/local/tomcat/webapps/ \
	-d \
	--restart unless-stopped \
	-t arm32v7/tomcat

Ejecutamos los siguientes comandos:
	docker exec -it geoserver bash
	apt-get update
	apt install wget unzip
	cd /usr/local/tomcat/webapps
	wget https://kumisystems.dl.sourceforge.net/project/geoserver/GeoServer/2.18.0/geoserver-2.18.0-war.zip 
	unzip geoserver-2.18.0-war.zip
	rm -rf target/ *.txt geoserver-2.18.0-war.zip

Descargamos la extension geoserver-2.18.0-vectortiles-plugin.zip y la descomprimimos en la carpeta "/usr/local/tomcat/webapps/geoserver/WEB-INF/lib" del docker de GEOSERVER. Les damos propietario "chown root:root /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/*". Reiniciamos el docker de GEOSERVER.
	cd /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/
	wget https://sourceforge.net/projects/geoserver/files/GeoServer/2.18-RC/extensions/geoserver-2.18-RC-vectortiles-plugin.zip
	unzip geoserver-2.18-RC-vectortiles-plugin.zip
	exit
	docker restart geoserver
	
Vereficamos que ha funcionado correctamente accediendo a su web (puede tardar un rato y se puede ver que hace con "docker logs -f geoserver":
	- 	http://localhost:5431/geoserver/             Usuario: admin     Password: geoserver
	
A continuación creamos el espacio de trabajo:
	Vamos a "Espacios de trabajo" y "Agregar un nuevo espacio de trabajo"
	Escribimos "Name":Lugares y "URI del espacio de nombres":daw2020
	Vamos a "Almacenes de datos" y "Agregar nuevo almacén"
	Seleccionamos "Espacio de trabajo":Lugares y escribimos "Nombre del origen de datos":lugares_postgis    host:192.168.1.250   port:5432   database:jesus2020    user:jesus2020   passwd:jesus2020         y pulsamos "Guardar".
	Si todo ha funcionado correctamente, estamos en "Nueva capa" y pulsamos sobre "Publicar". 
	En "Encuadre nativo" ponemos la esquina noroeste Mix x : -3.670099  Min Y: 40.507342  Max X:  -3.607165        Max Y:40.561603
	Pulsamos sobre "Calcular desde el encuadre nativo".
	Pulsamos en "Guardar".
	Ya tenemos la capa creada, si vamos a "Previsualización de capas" y pulsamos sobre "OpenLayers" sobre la nuestra veremos representados nuestros puntos de la base de datos POSTGIS.
	
Otra cosa que debemos hacer es desactivar CORS para TOMCAT según el siguiente enlace https://docs.geoserver.org/latest/en/user/production/container.html .
	docker exec -it geoserver bash
	apt install nano
	nano /usr/local/tomcat/webapps/geoserver/WEB-INF/web.xml

#LEAFLET
En este punto, vamos a establecer la conexión entre LEAFLET y nuestro GEOSERVER.
Abrimos el codigo de la web primera.html en chrome y vemos que se ve el mapa del mundo correctamente.
Vamos a la web de "GEOSERVER" y "Capas", abrimos nuestra capa "lugares" y pulsamos sobre "Cacheado de Teselas" y activamos la opcion "application/vnd.mapbox-vector-tile"
Abrimos el codigo de la web segunda.html en chrome y vemos que se ve el mapa del mundo correctamente con los puntos insertados en el POSTGIS.
A partir de aqui tenemos todas las aplicaciones y servicios instalados necesarios y empezaremos a crear nuestra "Consola de Emergencias 112"

	 
#PYTHON
Ejecutamos:
sudo apt-get install python-pip python-pip libpq-dev
pip install psycopg2
pip install pygresql
pip install pandas
pip install requests
pip install web.py
pip install CherryPy
pip install Flask
pip install waitress

docker build -t tfg-server .

docker run --name tfg-server  \
	-v $HOME/docker/TFG/tfg-server:/code  \
	-e TZ=Europe/Madrid  \
	-p 5430:5000 \
	-d \
	--restart unless-stopped  \
	tfg-server

### FUENTES DE INFORMACIÓN
Tutoriales y recursos:
	#DOCKER
	-	https://www.atareao.es/como/docker-y-raspberry-instalar-docker-y-docker-compose/
	#POSTGRES y POSTGIS
	-	https://github.com/Tob1asDocker/rpi-postgresql-postgis
	-	https://live.osgeo.org/es/quickstart/postgis_quickstart.html
	-	https://geopois.com/blog/geoserver/distributed-application		
	
	#LEAFLET
	-	https://mappinggis.com/tag/leaflet/
	-	https://www.earder.com/tutorials/postgis_geoserver_leaflet/
	-	https://mappinggis.com/2017/09/crear-mapas-web-animados-con-leaflet/
	-	https://github.com/perliedman/leaflet-realtime
	
	#Para calculo de rutas en mapa
	-	http://www.liedman.net/leaflet-routing-machine/api/
	-	https://mappinggis.com/2016/08/calculo-de-rutas-en-un-mapa-web-de-leaflet/
	-	https://www.linkedin.com/pulse/find-optimal-route-using-google-maps-api-andre-cedras
	-	https://github.com/googlemaps/google-maps-services-python
	-	https://github.com/kovacsbalu/WazeRouteCalculator
	-	https://github.com/GIScience/openrouteservice-py

	-	https://realpython.com/simpy-simulating-with-python/#what-simulation-is
		
	-	https://es.stackoverflow.com/questions/77913/como-usar-variable-globales-en-python
	
	#uso correcto de passwords
	-	https://blog.codinghorror.com/youre-probably-storing-passwords-incorrectly/
	
	#python 
	-	https://poesiabinaria.net/2017/11/monta-microservicios-web-rapidamente-python-web-py/
	-	https://towardsdatascience.com/build-your-own-python-restful-web-service-840ed7766832           <--- y dockerizar el python
###AREA DE LA APLICACIONES
ESQUINA NOROESTE 40.561603, -3.670099
ESQUINA SUDESTE  40.507342, -3.607165
