import requests

respuesta = requests.get("https://api.agify.io/?name=lucia")
datos = respuesta.json()

print("Nombre:", datos["name"])
print("Edad estimada:", datos["age"])
