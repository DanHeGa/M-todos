import json
import os
from flask import Flask, jsonify, request, send_from_directory
from Integradora.Thompson import infix2postfix, postRe2NFA
from Integradora.NFAtoDFA import nfa_to_dfa, generate_dfa_svg, language_checker

#create new application
app = Flask(__name__)

currentDFA = None

# Ruta principal para servir index.html
@app.route("/")
def index():
    print("Hola")
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../Frontend'), 'index.html')

# Ruta para archivos estáticos (como CSS o JS)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../Frontend'), path)

# Ruta de la API
@app.route("/api/registros/generales")
def obtener_registros():
    return jsonify({"mensaje": "Aquí están los registros"})

@app.route("/convertor", methods=['POST']) #RE post from the user
def get_dfa_svg():
    try:
        # Obtener la expresión regular (regex) del cliente
        re = request.json.get('regex')
        
        # Ahora convierte a postfix
        postfix_re = infix2postfix(re)

        # Convertir la notación postfix a NFA
        nfa = postRe2NFA(postfix_re)
        
        # Obtener las claves (alfabeto) y las transiciones del NFA
        keys = nfa.get("alphabet", [])
        transitions = nfa.get("states", {})

        print("Postfix RE:", postfix_re)  # DEBUG
        print("NFA States (Transitions):", transitions)  # DEBUG
        print("NFA Alphabet (Keys):", keys)  # DEBUG
        
        # CORRECCIONES: # en lineas 51. 52 y 55, agregue 57 y 58 (tercer parametro)
        # Si el NFA tiene claves extra (como el estado inicial), las eliminamos
        # Asegúrate de que solo pases las transiciones a nfa_to_dfa()
        #if 'start' in transitions:
        #    start_state = transitions.pop('start')  # Elimina la clave 'start', si existe

        # Convertir el NFA a DFA (solo las transiciones y las claves del alfabeto)
        # dfa = nfa_to_dfa(transitions, keys)
        
        start_state = nfa.get("start", 0)
        dfa = nfa_to_dfa(transitions, keys, start_state)

        global currentDFA
        currentDFA = dfa
        
        # Generar el SVG para visualizar el DFA (por ahora solo un ejemplo)
        svg = generate_dfa_svg(dfa, "dfa_svg.svg")

        # Responder al cliente con el SVG generado
        return jsonify({"svg": svg})

    except Exception as e:
        # En caso de error, devolver un mensaje de error
        return jsonify({"error": str(e)}), 500


@app.route("/wordChecker", methods=['POST'])
def simulate_dfa():
    global currentDFA
    if currentDFA is None:
        return jsonify({"error": "DFA not initialized"}), 400
    word = request.json.get('word')
    belongs = language_checker(word, currentDFA)
    return jsonify({"inLanguage": belongs})

    
PORT = "2000"  

if __name__ == '__main__':
    print("Running on: http://localhost:" + PORT)
    app.run(debug=True, port=2000)
