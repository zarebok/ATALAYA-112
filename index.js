var map = L.map('map'),
    realtime = L.realtime({
        url: 'http://zarbok.ddns.net:5431/geoserver/Lugares/wms?service=WMS&version=1.1.0&request=GetMap&layers=Lugares%3Alugares&bbox=-3.661999%2C40.527693%2C-3.620484%2C40.547912&width=768&height=374&srs=EPSG%3A4326&styles=&format=geojson',
        crossOrigin: true,
        type: 'json'
		}, {
        interval: 3 * 1000,
        pointToLayer: function (feature, latlng) {
			if(feature.properties.tipo=='base') {
				console.log("FUNCIONA BASE");
				switch (feature.properties.color) {
					case "blue":
						var imageUrl="./img/bnacional.png";
					break;
					case "cyan":
						var imageUrl="./img/blocal.png";
					break;
					case "orange":
						var imageUrl="./img/bbomberos.png";
					break;
					case "red":
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
				marker.bindPopup('Nombre: ' + feature.properties.name +
                    '<br/> Color:' + feature.properties.color+
                    '<br/> Tipo:' + feature.properties.tipo);
				
				return marker;
			} else {
				console.log("FUNCIONA PATRULLA");
				switch (feature.properties.color) {
					case "blue":
						var imageUrl="./img/cnacional.png";
					break;
					case "cyan":
						var imageUrl="./img/clocal.png";
					break;
					case "orange":
						var imageUrl="./img/cbomberos.png";
					break;
					case "red":
						var imageUrl="./img/cambulancia.png";
					break;
					default:
						var imageUrl="./img/cbomberos.png";
					break;
				}
				var myIcon = L.icon({
					iconUrl: imageUrl,
					iconSize: [40, 40]
				});
				
				var marker = L.marker(latlng,{
					icon: myIcon,
					zIndexOffset:0,
					riseOnHover:true,
					opacity: 1
				});
				marker.bindPopup('Nombre: ' + feature.properties.name +
                    '<br/> Color:' + feature.properties.color+
                    '<br/> Tipo:' + feature.properties.tipo);
				
				return marker;
			}
        },
        getFeatureId: function(feature) { //ESTO SIRVE PARA DIFERENCIAS LAS MARCAS Y BORRAR Y REINCIAR. PARA BARCOS "NAME" SERIA "MMSI"
            return feature.properties.name;
        },
    }).addTo(map);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.Routing.control({
  waypoints: [
    L.latLng(40.540277, -3.635533),
    L.latLng(40.547547, -3.620484)
  ]
}).addTo(map);

map.setView([40.547141,-3.635533], 14);

/*realtime.on('update', function() {
    map.fitBounds(realtime.getBounds(), {maxZoom: 13});
});*/

