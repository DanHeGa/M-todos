'''
DFA que lee palabras con un número par de simbolos a
Q E a b

0   1 0
1   2 1
2   1 2
'''
#mas que un indice de caracteres en una palabra, o el caracter en si, ve los estados
#como el momento en el que te encuentras; es decir, aquel punto en que te deja el hecho 
#de que exista determinado caracter del alfabeto, de tal forma que puede llevarte a 
#un estado donde se acepta la palabar, o uno donde NO.

def dfa(palabra):
    #un diccionario de las transiciones de cada estado
    delta = [{"a": 1, "b": 0}, 
             {"a": 2, "b": 1}, 
             {"a": 1, "b": 2 }]
    estado = 0
    for simbolo in palabra:
        estado = delta[estado][simbolo]
    if estado == 2:
        print(f"La palabra {palabra} fue reconocida por el DFA.")
        return True
    else:
        print(f"La palabra {palabra} no fue reconocida por el DFA.")
        return False
    

#palabra = input("Ingrese una palabra: ")
#es_reconocida = dfa(palabra)

#NFA particulares
#NFA general
#funciones individuales
#condiccionelaes afuera para entrar a funciones


frase = "b=7"
#loop en cada linea del txt 
    #condicionales para separación de caracteres  ##ya tom alos negativos como parte del número
    #para especiales con que sea "(" o ")"
    #para comnetarios con que sea "//" y de ahi el resto de la linea es comnetario
    #para operadores es con que sea ese simbolo en particular "=+-*/^" ##eso si, cuidado que no haya dos /, porque si no seria comnetario
        #para negativos si NO hay num antes es un num negativo, y si sí hay num antes es signo de resta
    #soy entero
        #retornar que es entero
        #para reales con que exista un punto
            #pero si es negativo, afuerzas debe de estar el cero antes del punto (-0.49)
            #si hay una e despues del número, puede ver un num entero - o +
    ##caso por si no seequivoco :( ## #existe punto y hay nums despues 
        #si hay una e despues del número, puede ver un num entero - o + 
    #las variables deben de emepzar con una letra, podriamos usar hash?Eso seria como enseñar al compilador con casos de prueba?
        #una vez dentro puede ver tanto letras, números y underscore 
    
print(frase.split()) #no usar

#end of file te llvs al final, y end of line repite el ciclo