import json
from flask import Flask, jsonify, request, send_from_directory
from Integradora.Thompson import infix2postfix, postRe2NFA
from Integradora.NFAtoDFA import nfa_to_dfa, generate_dfa_svg, language_checker

#create new application
app = Flask(__name__)

# Ruta principal para servir index.html
@app.route("/")
def index():
    return send_from_directory('Frontend', 'index.html')

# Ruta para archivos estáticos (como CSS o JS)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('Frontend', path)

# Ruta de la API
@app.route("/api/registros/generales")
def obtener_registros():
    return jsonify({"mensaje": "Aquí están los registros"})

@app.route("/convertor", methods=['POST']) #RE post from the user
def get_dfa_svg():
    try:
        # Obtener la expresión regular (regex) del cliente
        re = request.json.get('regex')

        # Convertir la expresión regular a notación postfix
        postfix_re = infix2postfix(re)

        # Convertir la notación postfix a NFA
        nfa = postRe2NFA(postfix_re)
        
        # Obtener las claves (alfabeto) y las transiciones del NFA
        keys = nfa.get("alphabet", [])
        transitions = nfa.get("states", {})

        print("Postfix RE:", postfix_re)  # DEBUG
        print("NFA States (Transitions):", transitions)  # DEBUG
        print("NFA Alphabet (Keys):", keys)  # DEBUG

        # Si el NFA tiene claves extra (como el estado inicial), las eliminamos
        # Asegúrate de que solo pases las transiciones a nfa_to_dfa()
        if 'start' in transitions:
            start_state = transitions.pop('start')  # Elimina la clave 'start', si existe

        # Convertir el NFA a DFA (solo las transiciones y las claves del alfabeto)
        dfa = nfa_to_dfa(transitions, keys)

        # Generar el SVG para visualizar el DFA (por ahora solo un ejemplo)
        svg = generate_dfa_svg(dfa, "dfa_svg.svg")

        # Responder al cliente con el SVG generado
        return jsonify({"svg": svg})

    except Exception as e:
        # En caso de error, devolver un mensaje de error
        return jsonify({"error": str(e)}), 500


@app.route("/wordChecker", methods=['POST'])
def simulate_dfa():
    word = request.json.get('word')
    regex = request.json.get('regex')
    postfix_re = infix2postfix(regex)
    nfa = postRe2NFA(postfix_re)
    keys = nfa["alphabet"]
    dfa = nfa_to_dfa(nfa["states"], keys)
    belongs = language_checker(word, regex)
    return jsonify({"inLanguage": belongs})

    
PORT = "2000"  

if __name__ == '__main__':
    print("Running on: http://localhost:" + PORT)
    app.run(debug=True, port=2000)
