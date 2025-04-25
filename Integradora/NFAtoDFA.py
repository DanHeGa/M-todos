from collections import deque

'''
# Esta es la salida del NFA de Dany:
keys = ['e', 'A', 'D', 'C', 'B']
originalNFA = [
    {'A': 1}, {}, {'B': 3}, {'e': (2, 5)}, {'e': (2, 5)}, {},
    {'C': 7}, {'e': 13}, {'D': 9}, {'e': (8, 11)}, {'e': (8, 11)},
    {'e': 13}, {'e': (6, 10)}, {}
]

'''
# Esta es la salida del NFA de Dany:
keys = ['e', 'A', 'D', 'C', 'B']
originalNFA = [
    {'A': 1}, {}, {'B': 3}, {'e': (2, 5)}, {'e': (2, 5)}, {},
    {'C': 7}, {'e': 13}, {'D': 9}, {'e': (8, 11)}, {'e': (8, 11)},
    {'e': 13}, {'e': (6, 10)}, {}
]
keys = ['e', 'a', 'b', 'c']
originalNFA = [
    {'a': 1}, {'e': (2, 4)}, {'b': 3}, {}, {'c': 5}, {}
]


# Cambia el NFA de la salida anterior a una tabla con las transiciones
# Guarda como listas de destinos
nfa = {}
for i, transiciones in enumerate(originalNFA):
    nfa[i] = {}
    for sym, dest in transiciones.items():
        if isinstance(dest, int):
            nfa[i][sym] = [dest]
        else:
            nfa[i][sym] = list(dest)

# Define el alfabeto, omitiendo el 'e' del simbolo de entrada
# Alfabeto sin 'e'
alfabeto = [k for k in keys if k != 'e']
startState = 0
acceptState = {i for i, transiciones in enumerate(originalNFA) if not transiciones}

# Encuentra los estados alcanzables por transiciones epsilon
def transicionesEpsilon(states):
    stack = list(states)
    closure = set(states)

    # Recorre los destinos epsilon
    while stack:
        state = stack.pop()
        for nextState in nfa.get(state, {}).get('e', []):
            if nextState not in closure:
                closure.add(nextState)
                stack.append(nextState)
    return closure

# Encuentra los estados alcanzables por simbolos especificos (que nos sean epsilon)
def transicionesSimbolos(states, symbol):
    result = set()
    for state in states:
        for dest in nfa.get(state, {}).get(symbol, []):
            result.add(dest)
    return result

# Define variables para empezar la conversion
dfaStates = []
dfaTransitions = {}
dfaFinalState = []
visto = set()

# Usar para el estado inicial la funcion transicionesEpsilon
start = frozenset(transicionesEpsilon([startState]))
queue = deque([start])
visto.add(start)

# Aplica el algoritmo de subconjuntos
while queue:
    current = queue.popleft()
    dfaStates.append(current)

    for symbol in alfabeto: # Se intenta mover con cada simbolo del alfabeto
        movimiento = transicionesSimbolos(current, symbol)
        estadosAlcanzables = transicionesEpsilon(movimiento) # aplica transicionesEpsilon despues de cada movimiento
        conjuntoEstados = frozenset(estadosAlcanzables)

        dfaTransitions[(current, symbol)] = conjuntoEstados # Conjunto de transiciones para el DFA

        # Agregar conjuntoEstados a la fila si no se ha visto, para procesar despues
        if conjuntoEstados not in visto:
            visto.add(conjuntoEstados)
            queue.append(conjuntoEstados)


# Toma como estado final del AFD cualquier conjunto de estados del DFA que contenga el estado final del AFN
for state in dfaStates:
    if any(s in acceptState for s in state):
        dfaFinalState.append(state)


# Imprime resultados
imprimeEstados = []
for i in range(len(dfaStates)):
    imprimeEstados.append("Q" + str(i) + ":" + str(sorted(dfaStates[i])))
print("Estados del AFD: " + " , ".join(imprimeEstados))

imprimeTransiciones = []
for key in dfaTransitions:
    src = sorted(list(key[0]))
    sym = key[1]
    dest = sorted(dfaTransitions[key])
    imprimeTransiciones.append(str(src) + " --" + str(sym) + "--> " + str(dest))
print("Transiciones del AFD: " + " , ".join(imprimeTransiciones))

print("Estado inicial del AFD: " + str(sorted(start)))

imprimeEstadosFinales = [str(sorted(state)) for state in dfaFinalState]
print("Estados finales del AFD: " + " , ".join(imprimeEstadosFinales))

