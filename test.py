linea = "78 a 4 b6"
l2 = "a = 32.4 *(-8.6 - b)/       6.1E-8"
l3 = "-6.8e75 -6 c"

lo = list(linea)
entero = [] #number mngt
for i in range(len(lo)):
    if lo[i] == '-' and lo[i + 1].isdigit():
        entero.append(lo[i])
    elif lo[i].isdigit():
        entero.append(lo[i])
        if i < len(lo) - 1 and not lo[i + 1].isdigit():
            if lo[i + 1] == '.':
                entero.append(lo[i + 1])
            elif lo[i + 1] in 'Ee': #identificar exponencial
                entero.append(lo[i + 1])
                if i + 2 < len(lo) and (lo[i + 2].isdigit() or lo[i + 2] == '-'):
                    while i + 1 < len(lo) and lo[i + 1].isdigit():
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
            if '.' in numero:
               print(f"{numero} float")
            else:
                print(f"{numero} Int")
    else:
        continue
  