<?php
session_start();
?>
<html>
<head>
    <title>ATALAYA-112: Consola de Usuario</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
	
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet-src.js"></script>	
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="./dist/leaflet-realtime.js"></script>
	<script src="./dist/leaflet.routing/leaflet-routing-machine.js"></script>
	<link rel="stylesheet" href="./dist/leaflet.routing/leaflet-routing-machine.css" />
	<script src="./src/leaflet-search.js"></script>
	<link rel="stylesheet" href="./src/leaflet-search.css" />	
	<link rel="stylesheet" href="./css/Control.Geocoder.css" />
	<script src="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"></script>	
	<link rel="stylesheet" href="./css/console.css" /> 	
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>


	
<script>
/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
var abierto = false;
var map;
let mensajes = [];
// getting all the markers at once
function getAllMarkers() {

    var allMarkersObjArray = []; // for marker objects
    var allMarkersGeoJsonArray = []; // for readable geoJson markers

    $.each(map._layers, function (ml) {

        if (map._layers[ml].feature) {

            allMarkersObjArray.push(this)
            allMarkersGeoJsonArray.push(JSON.stringify(this.toGeoJSON()))
        }
    })

    //console.log(allMarkersObjArray);
}



function centrarmapa(name) {
	var latlng;
	patrullas.forEach(function (arrayItem) {
		if(arrayItem.feature.properties.name==name) {
			markerlocal=arrayItem;
			latlng = arrayItem.getLatLng();
		}
	});
	map.setView([latlng.lat,latlng.lng], 20);
}


function finservicio(name,cuerpo) {
	var latlng;
	patrullas.forEach(function (arrayItem) {
		if(arrayItem.feature.properties.name==name) {
			markerlocal=arrayItem;
			latlng = arrayItem.getLatLng();
		}
	});
	//SELECT p1.name,p2.name,ST_DistanceSphere(p1.geom,p2.geom) FROM lugares AS p1, lugares AS p2 WHERE p1.id > p2.id;
	map.setView([latlng.lat,latlng.lng], 20);
}

function mensajeria() {
    $.ajax({
        url : 'https://zarbok.ddns.net:5430/resultado',
        type : 'POST',
        data : 'opcion=damemensajes&ultimo='+mensajes.length,
		success: function(response){
			for (let value of response.split("]")) {
				mensaje=value.substring(2);
				if(mensaje.length>0) {
					mensajes.push(mensaje);
					console.log("Mensaje nuevo: "+mensaje);
					document.getElementById("nummensajes").innerHTML=parseInt(document.getElementById("nummensajes").innerHTML)+1
					document.getElementById("buttonnoti").className = 'btn btn-primary';
				}
			}
		},error: function() {
			console.log("Error cargando mensajeria: "+response);
			//document.getElementById("necpatrol").innerHTML ="Se desconoce las patrullas necesarias.";
		}	
    });		
	setTimeout(mensajeria, 5000);
}

setTimeout(mensajeria, 5000);


function openNav() {
	if(abierto==false) {
		document.getElementById("mySidebar").style.width = "250px";
		document.getElementById("zonatrabajo").style.width = document.getElementById("zonatrabajo").offsetWidth - 250;
		document.getElementById("mySidebar").style.marginTop = document.getElementById("barrasup").offsetHeight;
		document.getElementById("zonatrabajo").style.marginLeft = "250px";
		abierto=true;
	} else {
		document.getElementById("mySidebar").style.width = "0";
		document.getElementById("zonatrabajo").style.marginLeft = "0";
		document.getElementById("zonatrabajo").style.width = document.getElementById("zonatrabajo").offsetWidth + 250;
		abierto=false;
	}
	$('.popover').popover('hide');
// any html element such as button, div to call the function()
getAllMarkers();	
}

function cardmensajeria() {
	if(abierto==true) {
		openNav();
	}
	document.getElementById("nummensajes").innerHTML=0
	document.getElementById("buttonnoti").className = 'btn btn-secondary';
	document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-dark" style="width: 18rem;" id="card1">';


	document.getElementById("card1").innerHTML += '   <div class="card-body" id="card2" style="width:87%">';
	document.getElementById("card2").innerHTML += '   <center><h5 class="card-title text-white">Notificaciones</h5></center>';
	document.getElementById("card2").innerHTML += '   <div data-spy="scroll" data-target="#navbar-example2" data-offset="0" id="scro"></div>';

	var reversed = mensajes.reverse();
	for (let element of reversed) {
		fecha=element.split(',')[1];
		msj=element.split(',')[2];
		fecha=fecha.substring(2);
		fecha=fecha.slice(0, -1)
		msj=msj.substring(2);
		msj=msj.slice(0, -1);
		msj=msj.replace("'", "")
		document.getElementById("scro").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">'+fecha+'</h6>';
		document.getElementById("scro").innerHTML += '	  <p class="card-text">'+msj+'</p>';
	}
	
	openNav();
}

function cardpatrulla(id,name,imagen,cuerpo,cometido,markerid) {
	if(abierto==true) {
		openNav();
	}

	switch(cuerpo) {
		case "nacional":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-info" style="width: 18rem;" id="card1">';
		break;
		case "local":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-primary" style="width: 18rem;" id="card1">';
		break;
		case "bombero":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-warning" style="width: 18rem;" id="card1">';
		break;		
		case "sanidad":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-danger" style="width: 18rem;" id="card1">';
		break;
		default:
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-dark" style="width: 18rem;" id="card1">';
		break;		
	}

	document.getElementById("card1").innerHTML += '   <form id="formservicio" ><div class="card-body" id="card2" style="width:87%">';
	document.getElementById("card2").innerHTML += '   <center><img class="card-img-top" src="'+imagen+'" style="width: 30%;" alt="Card image cap"></center>';
	document.getElementById("card2").innerHTML += '	  <center><h5 class="card-title text-white">'+name+'</h5></center><input type="hidden" id="opcionname" name="opcionname" value="'+name+'"><input type="hidden" id="opcioncuerpo" name="opcioncuerpo" value="'+cuerpo+'">';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white"><div id="cometidotext">Estado: '+cometido+'</div></h6>';
	//document.getElementById("card2").innerHTML += '	  <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card\'s content.</p>';
	//document.getElementById("card2").innerHTML += '	  <a href="#" class="btn btn-primary btn-sm border-dark text-white">Ir a:</a>';
	document.getElementById("card2").innerHTML += '	  <a onclick="javascript:centrarmapa(\''+name+'\');" class="btn btn-success btn-sm border-dark text-white">Ver en mapa</a>';
	document.getElementById("card2").innerHTML += '	  <input type="hidden" id="opcionid" value="'+id+'" name="opcionid"><input type="hidden" id="opcion" value="finservicio" name="opcion"><a id="finservicio" class="btn btn-danger btn-sm border-dark text-white">Fin servicio</a></form>';

    $('#finservicio').on('click', function( event ) {
        event.preventDefault();
		console.log('Nombre: ' + MaysPrimera(name) +
                    '<br/> Cuerpo: ' + MaysPrimera(cuerpo)+
                    '<br/> Cometido: Fin de Servicio' +
					"<a class='dropdown-item' id='div"+name+"' onclick='javascript:cardpatrulla(\""+id+"\",\""+name+"\",\""+imagen+"\",\""+cuerpo+"\",\""+MaysPrimera("Fin de Servicio")+"\",\""+markerid+"\")'>Ver patrulla</a>");
		patrullas[markerid].bindPopup('Nombre: ' + MaysPrimera(name) +
                    '<br/> Cuerpo: ' + MaysPrimera(cuerpo)+
                    '<br/> Cometido: Fin de Servicio' +
					"<a class='dropdown-item' id='div"+name+"' onclick='javascript:cardpatrulla(\""+id+"\",\""+name+"\",\""+imagen+"\",\""+cuerpo+"\",\""+MaysPrimera("Fin de Servicio")+"\",\""+markerid+"\")'>Ver patrulla</a>");                		
		document.getElementById("cometidotext").innerHTML='Estado: Fin de servicio';
		var namediv = name.replace(/\s/g, '');
		var elem = document.getElementById("div" +namediv);
		elem.remove();		
        $.ajax({
            url : 'https://zarbok.ddns.net:5430/resultado',
            type : 'POST',
            data : $('#formservicio').serialize(),
			success: function(response){
				console.log("Correcto: "+response);
			},error: function() {
				console.log("Error"+response);
			}	
        });
    });	
	
	openNav();
}
	
function cardincidencia(id,name,imagen,cuerpo,cometido,markerid) {
	if(abierto==true) {
		openNav();
	}
	
	switch(cuerpo) {
		case "nacional":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-info" style="width: 18rem;" id="card1">';
		break;
		case "local":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-primary" style="width: 18rem;" id="card1">';
		break;
		case "bombero":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-warning" style="width: 18rem;" id="card1">';
		break;		
		case "sanidad":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-danger" style="width: 18rem;" id="card1">';
		break;
		default:
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-dark" style="width: 18rem;" id="card1">';
		break;		
	}

	document.getElementById("card1").innerHTML += ' <div class="card-body" id="card2" style="width:87%">';
	document.getElementById("card2").innerHTML += '   <center><img class="card-img-top" src="'+imagen+'" style="width: 30%;" alt="Card image cap"></center>';
	document.getElementById("card2").innerHTML += '	  <center><h5 class="card-title text-white">'+MaysPrimera(name)+'</h5></center>';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Descripción: '+MaysPrimera(cometido)+'</h6>';
	
	document.getElementById("card2").innerHTML += '	  <p class="card-text">Patrullas necesarias:</p><form id="formdametarea" ><input type="hidden" id="opcionid" value="'+id+'" name="opcionid"><input type="hidden" id="opcion" value="dame_tarea" name="opcion"><ul class="card-text" id="necpatrol">Pendiente<div></form>';	


    $.ajax({
        url : 'https://zarbok.ddns.net:5430/resultado',
        type : 'POST',
        data : $('#formdametarea').serialize(),
		success: function(response){
			//console.log( $('#formdametarea').serialize() );
			response.split("'");
			x=0;
			anterior='';
			for (let value of response.split("'")) {
			  if(x==1) {
				texto ="<li>"+MaysPrimera(value)+": ";
				anterior=value;
			  }
			  if(x==3 || x==7 || x==11) {
				texto +='<button type="button" id="divpoper'+x+'" class="btn btn-secondary" onclick="pidepatrullas('+id+','+x+',\''+anterior+'\')" > '+MaysPrimera(value)+'</button></li><br>';

			  }			  
			  if(x==5 || x==9) {
				texto +="<li>"+MaysPrimera(value)+": ";
				anterior=value;
			  }					  
			  x += 1;
			}
			document.getElementById("necpatrol").innerHTML  = texto;
				//$('#divpoper3') //, #divpoper7, #divpoper11
			    
				$('#divpoper3').popover({
					title: 'Patrullas disponibles</button>',
					placement: 'bottom',
					html: true,
					content: '<div id="divpoper3texto">No disponible.</div>'
				});
				//$('#divpoper3').onclick = pidepatrullas(id,$('#divpoper3texto'));				
				
				$('#divpoper7').popover({
					title: 'Patrullas disponibles',
					placement: 'bottom',
					html: true,
					content: '<div id="divpoper7texto">No disponible.</div>'
				});
				//$('#divpoper7').onclick = pidepatrullas(id,$('#divpoper7'));				
					
				$('#divpoper11').popover({
					title: 'Patrullas disponibles',
					placement: 'bottom',
					html: true,
					content: '<div id="divpoper11texto">No disponible.</div>'
				});
				//$('#divpoper11').onclick = pidepatrullas(id,$('#divpoper11'));		
	
		},error: function() {
			console.log("Error cargando patrullas: "+response);
			document.getElementById("necpatrol").innerHTML ="Se desconoce las patrullas necesarias.";
		}	
    });	
	
	//document.getElementById("card2").innerHTML += '	  <a id="botonenviar" onclick="pidepatrullas('+id+')" class="btn btn-primary btn-sm border-dark text-white">Enviar a:</a>';
	document.getElementById("card2").innerHTML += '	  <a onclick="javascript:centrarmapa(\''+name+'\');" class="btn btn-success btn-sm border-dark text-white">Ver en mapa</a>';
	//document.getElementById("card2").innerHTML += '	  <a href="#" class="btn btn-danger btn-sm border-dark text-white">Fin servicio</a>';
	openNav();
}	

function pidepatrullas(id,esto,tipo) {
	var result;
	$.ajax({
		url : 'https://zarbok.ddns.net:5430/resultado',
		type : 'POST',
		data : 'opcionid='+id+'&opcion=dame_patrullas&opciontipo='+tipo,
		success: function(response){
			result = JSON.parse(response);
			chu="#divpoper"+esto+"texto";
			//console.log(chu + response);
			//console.log(result);
			$(chu)[0].innerHTML ="";
			result.forEach(element => $(chu)[0].innerHTML +='<a id="enviapatrulla" onclick="enviapatrullas('+id+','+element["id2"]+','+esto+', \''+element["name"]+'\',\''+tipo+'\')" class="badge bg-primary text-white">'+element["name"]+" a "+(Math.trunc(element["st_distancesphere"])/1000)+" km</a><br>");
		},error: function() {
			console.log("Error cargando patrullas: "+response);
			$("#divpoper"+esto+"texto")[0].innerHTML = "Error cargando patrullas: "+response;
			result = "Se desconoce las patrullas necesarias.";
		}	
		});	
	//return result;
}

function enviapatrullas(id,id2,cuadro,name,tipo) {
	var result;
	$.ajax({
		url : 'https://zarbok.ddns.net:5430/resultado',
		type : 'POST',
		data : 'opcionid='+id+'&opcion=enviapatrullas&opcionid2='+id2+'&opciontipo='+tipo,
		success: function(response){
			//result = JSON.parse(response);
			chu="#divpoper"+cuadro;
			console.log(chu + response);
			//console.log(result);
			$('#enviapatrulla').parent().parent().parent().popover('hide');
			$(chu)[0].innerHTML =name;
			//result.forEach(element => $(chu)[0].innerHTML +='<a id="enviapatrulla" onclick="enviapatrullas('+id+')" class="badge bg-primary text-white">'+element["name"]+" a "+(Math.trunc(element["st_distancesphere"])/1000)+" km</a><br>");
		},error: function() {
			console.log("Error cargando patrullas: "+response);
			$("#divpoper"+esto+"texto")[0].innerHTML = "Error cargando patrullas: "+response;
			result = "Se desconoce las patrullas necesarias.";
		}	
		});	
	//return result;
}

function menuincidencia(lat,lng,popup) {
	if(abierto==true) {
		openNav();
	}

	/*switch(cuerpo) {
		case "nacional":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-info" style="width: 18rem;" id="card1">';
		break;
		case "local":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-primary" style="width: 18rem;" id="card1">';
		break;
		case "bombero":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-warning" style="width: 18rem;" id="card1">';
		break;		
		case "sanidad":
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-danger" style="width: 18rem;" id="card1">';
		break;
		default:
			document.getElementById("barralateral").innerHTML = '<div class="card text-white bg-dark" style="width: 18rem;" id="card1">';
		break;		
	}*/
	document.getElementById("barralateral").innerHTML = '<form id="addincidencia" ><input type="hidden" id="opcion" value="66" name="opcion"><div class="card text-white bg-info" style="width: 18rem;" id="card1">';
	document.getElementById("card1").innerHTML += ' <div class="card-body" id="card2" style="width:87%">';
	document.getElementById("card2").innerHTML += '   <center><img class="card-img-top" src="img/icono.png" style="width: 30%;" alt="Card image cap"></center>';
	document.getElementById("card2").innerHTML += '	  <center><h5 class="card-title text-white">Nueva incidencia</h5></center>';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Latitud: '+(Math.round((lat.toString())*1000000)/1000000)+'<input type="hidden" id="opcionlat" value="'+lat+'" name="opcionlat"></h6>';	
		document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Longitud: '+(Math.round((lng.toString())*1000000)/1000000)+'<input type="hidden" id="opcionlong" value="'+lng+'" name="opcionlong"></h6>';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Titulo: <input type="text" id="opcionname" name="opcionname"></h6>';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Tipo: <select name="opcioncuerpo"><option value="ladron">Robo</option><option value="incendio">Incendio</option><option value="herido">Herido</option><option value="trafico">Tráfico</option><option value="terremoto">Terremoto</option><option value="pelea">Pelea</option><option value="vdg">Violencia de genero</option><option value="virus">Virus</option></select></h6>';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Descripción: </h6>';
	document.getElementById("card2").innerHTML += '	  <textarea class="card-text" id="opcioncometido" name="opcioncometido" rows="4" cols="27"> </textarea>';
	/*document.getElementById("card2").innerHTML += '	  <a href="#" class="btn btn-primary btn-sm border-dark text-white">Ir a:</a>';
	document.getElementById("card2").innerHTML += '	  <a onclick="javascript:centrarmapa(\''+name+'\');" class="btn btn-success btn-sm border-dark text-white">Ver en mapa</a>';*/
	document.getElementById("card2").innerHTML += '	  <input type="hidden" id="opcionid"  name="opcionid"><a id="enviarform" onclick="openNav();" class="btn btn-danger btn-sm border-dark text-white">Crear</a></form>';
    $('#enviarform').on('click', function( event ) {
        event.preventDefault();
        $.ajax({
            url : 'https://zarbok.ddns.net:5430/resultado',
            type : 'POST',
            data : $('#addincidencia').serialize(),
			success: function(response){
				console.log("Correcto: "+response);
			},error: function() {
				console.log("Error"+response);
			}	
        });
    });

	openNav();
}	

function menupatrulla(lat,lng,icono,cuerpo,popup) {
	if(abierto==true) {
		openNav();
	}

	switch(cuerpo) {
		case "nacional":
			document.getElementById("barralateral").innerHTML = '<form id="addpatrulla" ><div class="card text-white bg-info" style="width: 18rem;" id="card1">';
		break;
		case "local":
			document.getElementById("barralateral").innerHTML = '<form id="addpatrulla" ><div class="card text-white bg-primary" style="width: 18rem;" id="card1">';
		break;
		case "bombero":
			document.getElementById("barralateral").innerHTML = '<form id="addpatrulla" ><div class="card text-white bg-warning" style="width: 18rem;" id="card1">';
		break;		
		case "sanidad":
			document.getElementById("barralateral").innerHTML = '<form id="addpatrulla" ><div class="card text-white bg-danger" style="width: 18rem;" id="card1">';
		break;
		default:
			document.getElementById("barralateral").innerHTML = '<form id="addpatrulla" ><div class="card text-white bg-dark" style="width: 18rem;" id="card1">';
		break;		
	}
	document.getElementById("card1").innerHTML += ' <div class="card-body" id="card2" style="width:87%">';
	document.getElementById("card2").innerHTML += '<input type="hidden" id="opcion" value="22" name="opcion">';	
	document.getElementById("card2").innerHTML += '   <center><img class="card-img-top" src="'+icono+'" style="width: 30%;" alt="Card image cap"></center>';
	document.getElementById("card2").innerHTML += '	  <center><h5 class="card-title text-white">Nueva patrulla</h5></center>';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Latitud: '+(Math.round((lat.toString())*1000000)/1000000)+'<input type="hidden" id="opcionlat" value="'+lat+'" name="opcionlat"></h6>';	
		document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Longitud: '+(Math.round((lng.toString())*1000000)/1000000)+'<input type="hidden" id="opcionlong" value="'+lng+'" name="opcionlong"></h6>';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Nombre: <input type="text" id="opcionname" name="opcionname"></h6>';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Tipo: <input type="hidden" id="opcioncuerpo" value="'+cuerpo+'" name="opcioncuerpo">'+cuerpo+'</h6>';
	document.getElementById("card2").innerHTML += '	  <h6 class="card-subtitle mb-2 text-white">Tarea: <select name="opcioncometido" id="opcioncometido"><option value="patrullando" selected>Patrullando</option><option value="espera">En espera</option><option value=""></option></select></h6>';
	/*document.getElementById("card2").innerHTML += '	  <textarea class="card-text" id="opcioncometido" name="opcioncometido" rows="4" cols="27"> </textarea>';
	document.getElementById("card2").innerHTML += '	  <a href="#" class="btn btn-primary btn-sm border-dark text-white">Ir a:</a>';
	document.getElementById("card2").innerHTML += '	  <a onclick="javascript:centrarmapa(\''+name+'\');" class="btn btn-success btn-sm border-dark text-white">Ver en mapa</a>';*/
	document.getElementById("card2").innerHTML += '	  <a id="enviarformdos" onclick="openNav();" class="btn btn-danger btn-sm border-dark text-white">Crear</a></form>';
    $('#enviarformdos').on('click', function( event ) {
        event.preventDefault();
        $.ajax({
            url : 'https://zarbok.ddns.net:5430/resultado',
            type : 'POST',
            data : $('#addpatrulla').serialize(),
			success: function(response){
				console.log("Correcto: "+response);
			},error: function() {
				console.log("Error"+response);
			}			
        });
    });

	openNav();
}	
</script>
</head>
<body>
<?php

if (isset($_SESSION["k_username"])) {
 //echo 'Bienvenido';
}else{
 ?>
 <SCRIPT LANGUAGE="javascript">
	location.href = "https://zarbok.ddns.net/112-Emergencias/";
 </SCRIPT>
 <?php
 
}
?>
<nav class="navbar navbar-expand-sm bg-dark navbar-dark" id="barrasup">
  <ul class="navbar-nav">
   <a class="navbar-brand" href="#">
    <img src="img/icono.png" alt="Logo" style="width:40px;">
  </a>
    <li class="nav-item">
		<button type="button" class="btn btn-danger" onclick="javascript:location.href = 'https://zarbok.ddns.net/112-Emergencias/';">Logout</button>
    </li>
    <li class="nav-item">

    </li>
    <!-- Patrullas -->
    <li class="nav-item dropdown">
      <a class="nav-link dropdown-toggle" href="#" id="navbardrop" data-toggle="dropdown" >
        Patrullas
      </a>
      <div class="dropdown-menu" id="menupatrullas" style="z-index: 100;">
		
      </div>
    </li>
    <!-- Incidencias -->
    <li class="nav-item dropdown">
      <a class="nav-link dropdown-toggle" href="#" id="navbardrop" data-toggle="dropdown">
        Incidencias
      </a>
      <div class="dropdown-menu" id="menuincidencias">
      </div>
    </li>	
	<button id="buttonnoti" type="button" class="btn btn-secondary" onclick='javascript:cardmensajeria()'>
	  Notificaciones <span id="nummensajes" class="badge bg-secondary">0</span>
	</button>	
  </ul>
  <?php

if ($_SESSION["k_permiso"]==1) {


 ?>
  <ul class="navbar-nav ml-auto">

	<a class="nav-link" href="createuser.php" id="navbardrop" >
        Usuarios
      </a>
  </ul> 
  <?php

}
 ?>  
</nav>

	
	<div id="mySidebar" class="sidebar">
		<div id="cierre">
		<a href="javascript:void(0)" class="closebtn" onclick="openNav()">&times;</a>
		</div>
		<div id="barralateral">

		</div>
	</div>	
	<div class="row" id="zonatrabajo">
		<div id="map"  style="z-index: 1;"></div>
		<script src="js/console.js"></script>
	</div>
  

</body>
</html>