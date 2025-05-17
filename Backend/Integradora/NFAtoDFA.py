from collections import deque
from graphviz import Digraph
import regex as re
import ast

def convert_to_tableNFA(originalNFA):
    nfa = {}

    if isinstance(originalNFA, list):
        originalNFA = {i: trans for i, trans in enumerate(originalNFA)}

    for estado, transiciones in originalNFA.items():
        nfa[estado] = {}
        if isinstance(transiciones, list):
            for t in transiciones:
                for sym, dest in t.items():
                    if isinstance(dest, int):
                        nfa[estado].setdefault(sym, []).append(dest)
                    else:
                        nfa[estado].setdefault(sym, []).extend(dest)
        elif isinstance(transiciones, dict):
            for sym, dest in transiciones.items():
                if isinstance(dest, int):
                    nfa[estado][sym] = [dest]
                else:
                    nfa[estado][sym] = list(dest)
        else:
            raise TypeError(f"Transiciones para el estado {estado} no son válidas: {transiciones}")

    return nfa

def transicionesEpsilon(nfa, states):
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        epsilon_moves = nfa.get(state, {}).get('e', [])
        if isinstance(epsilon_moves, int):
            epsilon_moves = [epsilon_moves]
        for nextState in epsilon_moves:
            if nextState not in closure:
                closure.add(nextState)
                stack.append(nextState)
    return closure

def transicionesSimbolos(nfa, states, symbol):
    result = set()
    for state in states:
        for dest in nfa.get(state, {}).get(symbol, []):
            result.add(dest)
    return result

def nfa_to_dfa(originalNFA, keys, startState=0):
    nfa = convert_to_tableNFA(originalNFA)
    alfabeto = [k for k in keys if k != 'e']
    acceptState = {i for i, transiciones in enumerate(originalNFA) if not transiciones}

    dfaStates = []
    dfaTransitions = {}
    dfaFinalState = []
    visto = set()

    start = frozenset(transicionesEpsilon(nfa, [startState]))
    queue = deque([start])
    visto.add(start)

    while queue:
        current = queue.popleft()
        dfaStates.append(current)

        for symbol in alfabeto:
            movimiento = transicionesSimbolos(nfa, current, symbol)
            estadosAlcanzables = transicionesEpsilon(nfa, movimiento)
            conjuntoEstados = frozenset(estadosAlcanzables)
            dfaTransitions[(current, symbol)] = conjuntoEstados
            if conjuntoEstados not in visto:
                visto.add(conjuntoEstados)
                queue.append(conjuntoEstados)

    for state in dfaStates:
        if any(s in acceptState for s in state):
            dfaFinalState.append(state)

    resultDFA = {
        "estados": dfaStates,
        "transiciones": dfaTransitions,
        "estado_inicial": start,
        "estados_finales": dfaFinalState,
        "alfabeto": alfabeto
    }
    return resultDFA

def print_DFA(dfaStates, dfaTransitions, start, dfaFinalState):
    imprimeEstados = ["Q{}:{}".format(i, sorted(state)) for i, state in enumerate(dfaStates)]
    print("Estados del AFD: " + " , ".join(imprimeEstados))

    imprimeTransiciones = []
    for (origen, simbolo), destino in dfaTransitions.items():
        imprimeTransiciones.append(f"{sorted(origen)} --{simbolo}--> {sorted(destino)}")
    print("Transiciones del AFD: " + " , ".join(imprimeTransiciones))

    print("Estado inicial del AFD: " + str(sorted(start)))
    imprimeEstadosFinales = [str(sorted(state)) for state in dfaFinalState]
    print("Estados finales del AFD: " + " , ".join(imprimeEstadosFinales))

def generate_dfa_svg(dfa, output_file=None):
    dot = Digraph(format='svg')
    dot.attr(rankdir='LR')

    for estado in dfa["estados"]:
        nombre = etiquetaEstado(estado)
        shape = 'doublecircle' if estado in dfa["estados_finales"] else 'circle'
        dot.node(nombre, shape=shape)

    nombre_inicial = etiquetaEstado(dfa["estado_inicial"])
    dot.node('', shape='point')
    dot.edge('', nombre_inicial)

    for (origen, simbolo), destino in dfa["transiciones"].items():
        dot.edge(etiquetaEstado(origen), etiquetaEstado(destino), label=simbolo)

    return dot.pipe(format='svg').decode('utf-8')

def etiquetaEstado(estado):
    return "{" + ",".join(map(str, sorted(estado))) + "}"

def language_checker(word, dfa):
    current_state = dfa['estado_inicial']
    for symbol in word:
        if symbol not in dfa['alfabeto']:
            return False
        transition_key = (current_state, symbol)
        if transition_key in dfa['transiciones']:
            current_state = dfa['transiciones'][transition_key]
        else:
            return False
    return current_state in dfa['estados_finales']
