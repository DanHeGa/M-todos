
def letra(caracter): # Mayusculas y minusculas
    return (65 <= caracter <= 90) or (97 <= caracter <= 122)

def espacio(caracter):
    return caracter == 32
    
def lectorTokens(linea):
    for i in range(len(linea)):
        caracter = ord(linea[i]) # Cambia a ASCII.
        
        # Espacios
        if espacio(caracter):
            continue
        
        # Operadores + Parentesis
        elif caracter in (61, 43, 45, 42, 47, 94, 40, 41): 
            if (caracter == 61):
                print(chr(caracter)+"\t Asignacion")
            elif (caracter == 43):
                print(chr(caracter)+"\t Suma")
            elif (caracter == 45):
                print(chr(caracter)+"\t Resta")
            elif (caracter == 42):
                print(chr(caracter)+"\t Multiplicacion")
            elif (caracter == 47):
                print(chr(caracter)+"\t Division")
            elif (caracter == 94):
                print(chr(caracter)+"\t Potencia")
            elif (caracter == 40):
                print(chr(caracter)+"\t Parentesis que abre")
            elif (caracter == 41):
                print(chr(caracter)+"\t Parentesis que cierra")

        else:
            print("El caracter "+chr(caracter)+" no fue reconocido.")
    

datos = "a = 32.4 *(-8.6 - b)/       6.1E-8"
lectorTokens(datos)