def mostrarFicheros():
    i=1
    with open('nombre_fichero.txt', 'r') as fichero:
        for linea in fichero.readlines():
            print("Linea: ",i," ",linea, end='')
            i=i+1

def verContenido():
  with open('nombre_fichero.txt', 'r') as fichero:
        for linea in fichero.readlines():
            palabras = linea.split()
            print(f"Palabra:{palabras}")
            for palabra in palabras:
              print(palabra if palabra.isdigit())


if __name__ == '__main__':
    mostrarFicheros()
    verContenido()
