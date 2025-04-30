import json
from flask import Flask, jsonify, request
from Integradora.Thompson import infix2postfix, postRe2NFA
from Integradora.NFAtoDFA import nfa_to_dfa, generate_dfa_svg

#create new application
app = Flask(__name__)

@app.route('/')
def default():
    return "<h1> HomePage <h1>"

@app.route("/convertor", methods=['POST']) #RE post from the user
def get_dfa_svg():
    re = request.json.get('regex')
    
    #convert re to postfix
    postfix_re = infix2postfix(re)
    
    #convert postfix re to nfa
    nfa = postRe2NFA(postfix_re)
    
    #get nfa's keys and transitions
    keys = nfa["alphabet"]
    transitions = nfa["states"]
    print(postfix_re) #DEBUG
    
    #get dfa
    dfa = nfa_to_dfa(nfa, keys)
    
    #generate svg (TO DO)
    svg = generate_dfa_svg(dfa)
    
    return jsonify({
        "svg": svg
    })

@app.route("/wordChecker", method=['POST'])
def verificate_word():
    word = request.json.get('word')
    #function to analyze if a word goes within a specific language
    belongs = language_checker(word)
    
    return jsonify({
        "inLanguage":belongs
    })
    
    
  
PORT = "2000"  
if __name__ == '__main__':
    print("Running on: http://localhost:" + PORT)
    app.run(debug=True, port=2000)
