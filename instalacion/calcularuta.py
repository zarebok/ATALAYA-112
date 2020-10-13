import openrouteservice

coords = ((8.34234,48.23424),(8.34423,48.26424))

client = openrouteservice.Client(key='5b3ce3597851110001cf6248f2ed7abeb83047e6a74f5b73c4d2758d') # Specify your personal API key
routes = client.directions(coords)

print(routes)
