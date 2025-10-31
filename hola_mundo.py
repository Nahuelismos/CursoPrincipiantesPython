with open('frutas.txt', "r") as frutas:
    #print(frutas.readlines())
    for fruta_precio in frutas:
        linea = fruta_precio.split()
        if linea[0] == 'f':
           print(f"Fruta: {linea[1]} --> ${linea[2]} el kilo.")
        else:
           print(f"Verdura: {linea[1]} --> ${linea[2]} el kilo.")