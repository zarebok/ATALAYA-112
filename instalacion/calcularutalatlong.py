import openrouteservice
from openrouteservice import convert
import json

coords = ((-3.635017,40.540277),(-3.620484,40.534947))

client = openrouteservice.Client(key='5b3ce3597851110001cf6248f2ed7abeb83047e6a74f5b73c4d2758d') # Specify your personal API key

# decode_polyline needs the geometry only
geometry = client.directions(coords)['routes'][0]['geometry']

decoded = convert.decode_polyline(geometry)

print(json.dumps(decoded["coordinates"], indent=4, sort_keys=True))
