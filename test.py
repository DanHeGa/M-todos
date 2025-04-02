linea = "78 a 4 b6"
l2 = "a = 32.4 *(-8.6 - b)/       6.1E-8"
l3 = "6.8 75 6 c"

'''Ya verifica flotante, ahora necesita identificar si son negativos y el uso de exponenciales E y su exponente'''
lo = list(l2)
entero = [] #commnt
for i in range(len(lo)):
    if lo[i].isdigit():
        entero.append(lo[i])
        if i < len(lo) - 1 and not lo[i + 1].isdigit():
            if lo[i + 1] == '.':
                entero.append(lo[i + 1])
            else:
                if '.' in entero: #float identification
                    flt = "".join(entero)
                    print(f"{flt} float")
                    entero = []
                else:
                    numero = "".join(entero)
                    print(f"{numero} Int")
                    entero = []
        elif i == len(lo) - 1:
           numero = "".join(entero)
           print(f"{numero} Int")
    else:
        continue
  