def variable(caracter): # Mayusculas, minusculas y underscore
    return (65 <= caracter <= 90) or (97 <= caracter <= 122) or caracter == 95

def operadores(caracter): # Valor de los operadores en ASCII.
    return caracter in (61, 43, 45, 42, 47, 94, 40, 41)

def espacio(caracter):
    return caracter == 32

def digito(caracter): # Numeros del 0 a 9
    return 48 <= caracter <= 57  
    
def lectorOperadores(linea):
    i = 0
    while i < len(linea): #Necesito usar un while debido a las variables.
        caracter = ord(linea[i]) # Cambia a ASCII.
        
        # Espacios
        if espacio(caracter):
            i += 1
            continue

        # Comentarios
        elif caracter == 47 and i + 1 < len(linea) and ord(linea[i + 1]) == 47:
            print(f"{linea[i:].strip()}\tComentario")
            break
        
        # Variables
        elif variable(caracter):
            inicio = i
            while i < len(linea) and (variable(ord(linea[i])) or digito(ord(linea[i]))):
                i += 1
            print(f"{linea[inicio:i]}\tVariable")
            continue

        # Operadores + Parentesis
        elif operadores(caracter):
            key = {
                61: "Asignacion",
                43: "Suma",
                45: "Resta",
                42: "Multiplicacion",
                47: "Division",
                94: "Potencia",
                40: "Parentesis que abre",
                41: "Parentesis que cierra"
            }
            print(f"{chr(caracter)}\t{key[caracter]}")
            i += 1
            continue

        else:
            #print("El caracter "+chr(caracter)+" no fue reconocido.")
            i += 1

datos = "a_MyVar03=32.4*(-8.6 - b_var8)/       6.1E-8 //Esto es un = comentario" #Va a leer E como variable.
lectorOperadores(datos)
