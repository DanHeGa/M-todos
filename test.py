linea = "78 a 4 b6"
l2 = "a = 32.4 *(-8.6 - b)/       6.1E-8"
l3 = "-6.8e75 -6 c"
l4 = "a_MyVar03=32.4*(-8.6 - b_var8)/       6.1e-8 //Esto es un = comentario"

lo = l4
entero = [] #number mngt
i = 0
while i < len(lo):
    if lo[i] == '-' and lo[i + 1].isdigit():
        entero.append(lo[i])
        i += 1
    if lo[i].isdigit():
        entero.append(lo[i])
        if i < len(lo) - 1 and not lo[i + 1].isdigit():
            if lo[i + 1] == '.':
                entero.append(lo[i + 1])
                i += 1
                while i + 1 < len(lo) and lo[i + 1].isdigit():
                    i += 1
                    entero.append(lo[i])
                if lo[i + 1] in 'Ee': #identificar exponencial
                    entero.append(lo[i + 1])
                    i += 1
                    if i + 1 < len(lo) and (lo[i + 1].isdigit() or lo[i + 1] == '-'):
                        entero.append(lo[i + 1])
                        i += 1
                        while i + 1 < len(lo) and lo[i + 1].isdigit():
                            i += 1
                            entero.append(lo[i])
            num = "".join(entero)           
            if '.' in num or 'E' in num or 'e' in num:
                print(f"{num} float")
            else:
                print(f"{num} Int")
            entero = []
        elif i == len(lo) - 1:
            numero = "".join(entero)
            if '.' in numero:
               print(f"{numero} float")
            else:
                print(f"{numero} Int")
            entero = []          
    else:
        i += 1
        continue
    i += 1
  