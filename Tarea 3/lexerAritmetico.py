def variable(caracter): # Mayusculas, minusculas y underscore
    return (65 <= caracter <= 90) or (97 <= caracter <= 122) or caracter == 95

def operadores(caracter): # Valor de los operadores en ASCII.
    return caracter in (61, 43, 45, 42, 47, 94, 40, 41)

def espacio(caracter):
    return caracter == 32

def digito(caracter): # Numeros del 0 a 9
    return 48 <= caracter <= 57  
   

#lex main function
def lexerAritmetico(archivo):
    
    with open(archivo, "r") as file:
        lineas = file.readlines()
    
    for linea in lineas:
        lo = list(linea)
        entero = [] #number mngt
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
            
            # Números (enteros, flotantes, notación científica)
            elif digito(caracter) or (linea[i] == '-' and i + 1 < len(linea) and digito(ord(linea[i + 1]))):
                entero = []
                if linea[i] == '-':  # Detectar números negativos
                    entero.append(linea[i])
                    i += 1
                while i < len(linea) and (digito(ord(linea[i])) or linea[i] in '.Ee-'):
                    if linea[i] in 'Ee' and (i + 1 < len(linea) and (linea[i + 1].isdigit() or linea[i + 1] == '-')):
                        entero.append(linea[i])
                        i += 1
                    entero.append(linea[i])
                    i += 1
                num = "".join(entero)
                if '.' in num or 'E' in num or 'e' in num:
                    print(f"{num}\tFloat")
                else:
                    print(f"{num}\tInt")
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
    
            elif espacio(linea):
                continue        
            i += 1

lexerAritmetico("expresiones.txt")
