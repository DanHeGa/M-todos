from collections import deque
from graphviz import Digraph
import regex as re

'''
# Esta es la salida del NFA de Dany:
keys = ['e', 'A', 'D', 'C', 'B']
originalNFA = [
    {'A': 1}, {}, {'B': 3}, {'e': (2, 5)}, {'e': (2, 5)}, {},
    {'C': 7}, {'e': 13}, {'D': 9}, {'e': (8, 11)}, {'e': (8, 11)},
    {'e': 13}, {'e': (6, 10)}, {}
]
'''

def convert_to_tableNFA(originalNFA):
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
    return nfa

# Encuentra los estados alcanzables por transiciones epsilon
def transicionesEpsilon(nfa, states):
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
def transicionesSimbolos(nfa, states, symbol):
    result = set()
    for state in states:
        for dest in nfa.get(state, {}).get(symbol, []):
            result.add(dest)
    return result

def nfa_to_dfa(originalNFA, keys):
     # Define el alfabeto, omitiendo el 'e' del simbolo de entrada
    # Alfabeto sin 'e'
    nfa = convert_to_tableNFA(originalNFA)
    alfabeto = [k for k in keys if k != 'e']
    startState = 0
    acceptState = {i for i, transiciones in enumerate(originalNFA) if not transiciones}
    
    # Define variables para empezar la conversion
    dfaStates = []
    dfaTransitions = {}
    dfaFinalState = []
    visto = set()

    # Usar para el estado inicial la funcion transicionesEpsilon
    start = frozenset(transicionesEpsilon(nfa, [startState]))
    queue = deque([start])
    visto.add(start)

    # Aplica el algoritmo de subconjuntos
    while queue:
        current = queue.popleft()
        dfaStates.append(current)

        for symbol in alfabeto: # Se intenta mover con cada simbolo del alfabeto
            movimiento = transicionesSimbolos(nfa, current, symbol)
            estadosAlcanzables = transicionesEpsilon(nfa, movimiento) # aplica transicionesEpsilon despues de cada movimiento
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

    resultDFA = {
        "estados": dfaStates,
        "transiciones": dfaTransitions,
        "estado_inicial": start,
        "estados_finales": dfaFinalState
    }
    return resultDFA

def print_DFA(dfaStates, dfaTransitions, start, dfaFinalState):
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

def generate_dfa_svg(dfa, output_file):
    dot = Digraph(format='svg')
    dot.attr(rankdir='LR')

    # Estados q
    for estado in dfa["estados"]:
        nombre = etiquetaEstado(estado)
        shape = 'doublecircle' if estado in dfa["estados_finales"] else 'circle'
        dot.node(nombre, shape=shape)

    # q0
    nombre_inicial = etiquetaEstado(dfa["estado_inicial"])
    dot.node('', shape='point')
    dot.edge('', nombre_inicial)

    # Transiciones
    for (origen, simbolo), destino in dfa["transiciones"].items():
        origen_nombre = etiquetaEstado(origen)
        destino_nombre = etiquetaEstado(destino)
        dot.edge(origen_nombre, destino_nombre, label=simbolo)

    return dot.pipe(format='svg').decode('utf-8')


def etiquetaEstado(estado):
    return "{" + ",".join(map(str, sorted(estado))) + "}"

def language_checker(word, regular_expression):
    regex = re.compile(regular_expression)
    return bool(regex.fullmatch(word))
    
def main():   
    # Esta es la salida del NFA de Dany:
    keys = ['e', 'B', 'C', 'A']
    originalNFA = [{'A': 1}, {'e': 5}, {'B': 3}, {'e': 5}, 
                {'e': [0, 2]}, {'e': 8}, {'C': 7}, {'e': [6, 9]}, 
                {'e': [6, 9]}, {}]

    dfa = nfa_to_dfa(originalNFA, keys)

    states = dfa["estados"]
    transitions = dfa["transiciones"]
    initial_state = dfa["estado_inicial"]
    final_state = dfa["estados_finales"]

    generate_dfa_svg(dfa, "dfa_svg.svg")
    print_DFA(states, transitions, initial_state, final_state)
    
if __name__ == '__main__':
    main()
