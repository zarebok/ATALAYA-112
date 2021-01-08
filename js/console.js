patrullas = [];
function MaysPrimera(string){
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function addPatrullaMenu (id, name, imagen, cuerpo, cometido, markerid) { 
    if(typeof name == "string") {
        if($("#div" + name).length == 0) {
          // crea un nuevo div 
          // y aÃ±ade contenido 
		  var namediv = name.replace(/\s/g, '');
          var newDiv = document.createElement("div" + namediv); 
          newDiv.setAttribute("id", "helloButton");
          newDiv.innerHTML ="<a class='dropdown-item' id='div"+namediv+"' onclick='javascript:cardpatrulla(\""+id+"\",\""+name+"\",\""+imagen+"\",\""+cuerpo+"\",\""+MaysPrimera(cometido)+"\",\""+markerid+"\")'><img src="+imagen+" width='20' height='20'>"+MaysPrimera(name)+"</a>"; 
          //newDiv.appendChild(newContent); //aÃ±ade texto al div creado. 

          // aÃ±ade el elemento creado y su contenido al DOM 
          //var currentDiv = document.getElementById("menupatrullas"); 
          //document.body.insertBefore(newDiv, currentDiv); 
          //var originalDiv = document.getElementById("patrullavacio")
          var parentDiv = document.getElementById("menupatrullas");
          //parentDiv.insertBefore(newDiv, originalDiv.nextSibling);
          parentDiv.insertAdjacentHTML('beforeend', newDiv.innerHTML);
          console.log("Creo DIV de patrulla con ID "+id+" con MARKERID "+markerid+" porque no existe: " + name)
        } else {
            console.log("No creo DIV de patrulla con ID "+id+" con MARKERID "+markerid+" porque existe: " + name)
        
        }
    }
}

function addIncidenciaMenu (id, name, imagen, cuerpo, cometido, markerid) { 
    if(typeof name == "string") {
        if($("#div" + name).length == 0) {
          // crea un nuevo div 
          // y aÃ±ade contenido 
		  var namediv = name.replace(/\s/g, '');
          var newDiv = document.createElement("div" + namediv); 
          newDiv.setAttribute("id", "helloButton");
          newDiv.innerHTML ="<a class='dropdown-item' id='div"+namediv+"' onclick='javascript:cardincidencia(\""+id+"\",\""+name+"\",\""+imagen+"\",\""+cuerpo+"\",\""+MaysPrimera(cometido)+"\",\""+markerid+"\")'><img src="+imagen+" width='20' height='20'>"+MaysPrimera(name)+"</a>"; 
          //newDiv.appendChild(newContent); //aÃ±ade texto al div creado. 

          // aÃ±ade el elemento creado y su contenido al DOM 
          //var currentDiv = document.getElementById("menupatrullas"); 
          //document.body.insertBefore(newDiv, currentDiv); 
          //var originalDiv = document.getElementById("patrullavacio")
          var parentDiv = document.getElementById("menuincidencias");
          //parentDiv.insertBefore(newDiv, originalDiv.nextSibling);
          parentDiv.insertAdjacentHTML('beforeend', newDiv.innerHTML);
          console.log("Creo DIV de incidencia con ID "+id+" con MARKERID "+markerid+" porque no existe: " + name)
        } else {
            console.log("No creo DIV de incidencia con ID "+id+" con MARKERID "+markerid+" porque existe: " + name)
        
        }
    }
}

map = L.map('map'),
    realtime = L.realtime({
        //url: 'http://zarbok.ddns.net:5431/geoserver/Lugares/wms?service=WMS&version=1.1.0&request=GetMap&layers=Lugares%3Alugares&bbox=-3.670099%2C40.506342%2C-3.607165%2C40.562603&width=768&height=686&srs=EPSG%3A4326&styles=&format=geojson',
        url: 'https://zarbok.ddns.net:5443/geoserver/Lugares/wms?service=WMS&version=1.1.0&request=GetMap&layers=Lugares%3Alugares&bbox=-3.690099%2C40.486342%2C-3.587165%2C40.582603&width=768&height=686&srs=EPSG%3A4326&styles=&format=geojson',        
        crossOrigin: true,
        type: 'json'
        }, {
        interval: 1 * 1000,
        pointToLayer: function (feature, latlng) {
            if(feature.properties.tipo=='base') {
                //console.log("FUNCIONA BASE");
                switch (feature.properties.cuerpo) {
                    case "nacional":
                        var imageUrl="./img/bnacional.png";
                    break;
                    case "local":
                        var imageUrl="./img/blocal.png";
                    break;
                    case "bombero":
                        var imageUrl="./img/bbomberos.png";
                    break;
                    case "sanidad":
                        var imageUrl="./img/bhospital.png";
                    break;
                    default:
                        var imageUrl="./img/bhospital.png";
                    break;
                }
                var myIcon = L.icon({
                    iconUrl: imageUrl,
                    iconSize: [40, 40]
                });
                    
                var marker = L.marker(latlng,{
                    icon: myIcon,
                    opacity: 0.75
                    
                });
                //patrullas.push(marker);
				patrullas[L.stamp(marker)]=marker;
				marker.optionname=feature.properties.name;
				marker.optioncometido=feature.properties.cometido;
				marker.optioncuerpo=feature.properties.cuerpo;
				marker.optionimagen=feature.properties.imageUrl;
                marker.bindPopup('Nombre: ' + MaysPrimera(feature.properties.name) +
                    '<br/> Cuerpo: ' + MaysPrimera(feature.properties.cuerpo)+
					"<a class='dropdown-item' id='divmenuincidencia' onclick='javascript:menupatrulla(\""+latlng.lat+"\",\""+latlng.lng+"\",\""+imageUrl+"\",\""+feature.properties.cuerpo+"\",\""+L.stamp(marker)+"\");'>Solicitar Patrulla</a>");
                    //'<br/> Tipo: ' + feature.properties.tipo);
                
                return marker;
            } else if(feature.properties.tipo=='patrulla') {
                //console.log("PATRULLA:" + feature.properties.name);
                switch (feature.properties.cuerpo) {
                    case "nacional":
                        var imageUrl="./img/cnacional.png";
                    break;
                    case "local":
                        var imageUrl="./img/clocal.png";
                    break;
                    case "bombero":
                        var imageUrl="./img/cbomberos.png";
                    break;
                    case "sanidad":
                        var imageUrl="./img/cambulancia.png";
                    break;
                    default:
                        var imageUrl="./img/cbomberos.png";
                    break;
                }
                var myIcon = L.icon({
                    iconUrl: imageUrl,
                    iconSize: [40, 40],
                    //iconAnchor: [0, 40]  //el vertice de abajo marca el lugar exacto
                });
                
                var marker = L.marker(latlng,{
                    icon: myIcon,
                    zIndexOffset:0,
                    riseOnHover:true,
                    opacity: 1
                });
                //patrullas.push(marker);    
				patrullas[L.stamp(marker)]=marker;
				marker.optionname=feature.properties.name;
				marker.optioncometido=feature.properties.cometido;
				marker.optioncuerpo=feature.properties.cuerpo;
				marker.optionimagen=feature.properties.imageUrl;
                addPatrullaMenu(feature.properties.id,feature.properties.name,imageUrl,feature.properties.cuerpo,feature.properties.cometido,L.stamp(marker));
                marker.bindPopup('Nombre: ' + MaysPrimera(feature.properties.name) +
                    '<br/> Cuerpo: ' + MaysPrimera(feature.properties.cuerpo)+
                    '<br/> Cometido: ' + MaysPrimera(feature.properties.cometido)+
                    //'<br/> Tipo: ' + feature.properties.tipo+
					"<a class='dropdown-item' id='div"+feature.properties.name+"' onclick='javascript:cardpatrulla(\""+feature.properties.id+"\",\""+feature.properties.name+"\",\""+imageUrl+"\",\""+feature.properties.cuerpo+"\",\""+MaysPrimera(feature.properties.cometido)+"\",\""+L.stamp(marker)+"\")'>Ver patrulla</a>");                
                return marker;
            } else {
                //console.log("PATRULLA:" + feature.properties.name);
                switch (feature.properties.cuerpo) {
                    case "ladron":
                        var imageUrl="./img/robo.png";
                    break;
                    case "herido":
                        var imageUrl="./img/herido.png";
                    break;
                    case "incendio":
                        var imageUrl="./img/incendio.png";
                    break;
                    case "pelea":
                        var imageUrl="./img/pelea.png";
                    break;
                    case "terremoto":
                        var imageUrl="./img/terremoto.png";
                    break;
                    case "trafico":
                        var imageUrl="./img/trafico.png";
                    break;
                    case "virus":
                        var imageUrl="./img/virus.png";
                    break;              
                    case "vdg":
                        var imageUrl="./img/vdg.png";
                    break;      					
                    default:
                        var imageUrl="./img/cbomberos.png";
                    break;
                }
                var myIcon = L.icon({
                    iconUrl: imageUrl,
                    iconSize: [40, 40],
                    //iconAnchor: [0, 40]  //el vertice de abajo marca el lugar exacto
                });
                
                var marker = L.marker(latlng,{
                    icon: myIcon,
                    zIndexOffset:0,
                    riseOnHover:true,
                    opacity: 1
                });
                //patrullas.push(marker);    
				patrullas[L.stamp(marker)]=marker;
				marker.optionname=feature.properties.name;
				marker.optioncometido=feature.properties.cometido;
				marker.optioncuerpo=feature.properties.cuerpo;
				marker.optionimagen=feature.properties.imageUrl;
                addIncidenciaMenu(feature.properties.id,feature.properties.name,imageUrl,feature.properties.cuerpo,feature.properties.cometido,L.stamp(marker));
                marker.bindPopup('Nombre: ' + MaysPrimera(feature.properties.name) +
                    '<br/> Tipologia: ' + MaysPrimera(feature.properties.cuerpo)+
                    '<br/> Descripción: ' + MaysPrimera(feature.properties.cometido)+
                    //'<br/> Tipo: ' + feature.properties.tipo+
					"<a class='dropdown-item' id='div"+feature.properties.name+"' onclick='javascript:cardincidencia(\""+feature.properties.id+"\",\""+feature.properties.name+"\",\""+imageUrl+"\",\""+feature.properties.cuerpo+"\",\""+MaysPrimera(feature.properties.cometido)+"\",\""+L.stamp(marker)+"\")'>Ver incidencia</a>");

                return marker;
            }
        },
        getFeatureId: function(feature) { //ESTO SIRVE PARA DIFERENCIAS LAS MARCAS Y BORRAR Y REINCIAR. PARA BARCOS "NAME" SERIA "MMSI"
            return feature.properties.name;
        },
    }).addTo(map);


L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

/*L.Routing.control({
  waypoints: [
    L.latLng(40.540277, -3.635533),
    L.latLng(40.547547, -3.620484)
  ]
}).addTo(map);*/

//define rectangle geographical bounds
var bounds = [[40.561603, -3.670099], [40.507342, -3.607165]];

// create an orange rectangle
L.rectangle(bounds, {color: "#ff0000", weight: 2, fillOpacity: 0}).addTo(map);

map.setView([40.547141,-3.635533], 14);

var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng) // Sets the geographical point where the popup will open.
        .setContent("Coordenada:<br> " +  (Math.round((e.latlng.lat.toString())*1000000)/1000000) + "," +  (Math.round((e.latlng.lng.toString())*1000000)/1000000) + "<br><a class='dropdown-item' id='divmenuincidencia' onclick='javascript:menuincidencia(\""+e.latlng.lat+"\",\""+e.latlng.lng+"\");'>Crear Incidencia</a>") // Sets the HTML content of the popup.  PARA CERRAR POPUP $(\".leaflet-popup-close-button\")[0].click();
        .openOn(map); // Adds the popup to the map and closes the previous one. 
}

map.on('click', onMapClick);


var geocoder=L.Control.geocoder({
    defaultMarkGeocode: false,
    geocoder: new L.Control.Geocoder.Nominatim({
        geocodingQueryParams: {
            "viewbox": "-3.607165,40.507342,-3.670099,40.561603",  //Con esto limitamos la zona de busqueda de las direcciones a nuestro area
            "bounded": "1"
        }
    })
}).on('markgeocode', function(e) {
    popup
        .setLatLng(e.geocode.center) // Sets the geographical point where the popup will open.
        .setContent(e.geocode.name.split(",")[0] + "<br>" + e.geocode.html + "<br><a class='dropdown-item' id='divmenuincidencia' onclick='javascript:menuincidencia(\""+e.geocode.center.lat+"\",\""+e.geocode.center.lng+"\");'>Crear Incidencia</a><br>") // Sets the HTML content of the popup.
        .openOn(map); // Adds the popup to the map and closes the previous one.     
    map.fitBounds(e.geocode.center);
  });

geocoder.addTo(map);


/*realtime.on('update', function() {
    map.fitBounds(realtime.getBounds(), {maxZoom: 13});
});*/