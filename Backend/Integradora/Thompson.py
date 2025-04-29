import re
from graphviz import Digraph


def infix2postfix(regex):
  postFix = []
  stack = []
  precedence = {
    '^' : 5,
    '/': 4,
    '*': 4,
    '.': 3,
    '+': 2,
    '-': 2,
    '(': 1
  }
  
  associativity = {
    '^': 'RL',  # Derecha a izquierda
    '*': 'LR',   # Izquierda a derecha
    '/': 'LR',
    '+': 'LR',
    '-': 'LR',
    '.': 'LR'
  }
  
  for ele in regex:
    if ele == ' ':
      continue
    
    if ele not in "()^/*+-.":
      postFix.append(ele)
    elif ele == '(':
      stack.append(ele)
    elif ele == ')':
      fin = ''
      while fin != '(':
        fin = stack.pop()
        if fin != '(':
          postFix.append(fin)
    elif len(stack) > 0:
      if precedence[ele] > precedence[stack[-1]]:
        stack.append(ele)
      
      elif precedence[ele] < precedence[stack[-1]]: #current element precedence is lower than last element in stack precedence 
        while len(stack) > 0 and precedence[ele] < precedence[stack[-1]]:
            lastEle  =  stack.pop()
            postFix.append(lastEle)
        stack.append(ele)
      
      elif precedence[ele]  ==  precedence[stack[-1]]:
        if associativity[ele] == 'RL':
          stack.append(ele)
        elif associativity[ele] == 'LR':
          sameLastAsso  =  stack.pop()
          postFix.append(sameLastAsso)
          stack.append(ele)
    else:
      stack.append(ele)
  
  #pop out last stack elements
  while stack:
    postFix.append(stack.pop())
  
  postFix = ''.join(postFix)
  noBlanks = postFix.replace(" ", "")
  print(noBlanks)
  return noBlanks


def postRe2NFA(postfix):
  #waits for postfix re
  regex = ''.join(postfix)

  #abecedario, takes only the elements it sees in the expression 
  keys = list(set(re.sub('[^A-Za-z0-9]+', '', regex)+'e'))

  s = []
  stack = []
  start = 0
  end = 1
  
  #counter for states
  counter = -1 
  
  #classifier for the different states we will have
  c1 = 0 
  c2 = 0
 
 
 #lets say key is = AB*CD*+
  for i in regex:
      if i in keys:
          counter = counter+1;c1 = counter
          counter = counter+1;c2 = counter
          s.append({});s.append({}) #creates a dictionary for each state, so that each can have a transition
          stack.append([c1,c2]) 
          s[c1][i] = c2 #ex; s = [{1 : {'A' : 2}},{}]; es decir, 1---A--->2
      elif i == '*':
          r1,r2 = stack.pop()
          counter = counter+1;c1 = counter
          counter = counter+1;c2 = counter
          s.append({});s.append({}) 
          stack.append([c1,c2])
          s[r2]['e'] = [r1,c2]
          s[c1]['e'] = [r1,c2]
          if start == r1:start = c1 
          if end == r2:end = c2 
      elif i == '+':
        r1, r2 = stack.pop()
        counter += 1; c1 = counter
        counter += 1; c2 = counter
        s.append({}); s.append({})
        stack.append([c1, c2])
        s[r2]['e'] = [r1, c2]
        s[c1]['e'] = [r1]
      elif i == '.':
          #get last states in stack and unite them
          nfa21, nfa22 = stack.pop()
          nfa11, nfa12 = stack.pop()
          stack.append([nfa11, nfa22])
          s[nfa12]['e'] = nfa21
          if start == nfa21 : start = nfa11
          if end == nfa12 : end = nfa22     
      elif i == '|':
          counter = counter+1
          c1 = counter
          counter = counter+1
          c2 = counter
          s.append({})
          s.append({})
          r11,r12 = stack.pop()
          r21,r22 = stack.pop()
          stack.append([c1,c2])
          s[c1]['e'] = [r21,r11]
          s[r12]['e'] = c2
          s[r22]['e'] = c2
          if start == r11 or start == r21:start = c1 
          if end == r22 or end == r12:end = c2
  print (keys)
  print (s)
    
  return {
    "states": s,
    "start": start,
    "end": end,
    "alphabet": keys
  }
  
def main():
  # Example expression that should result in a DFA with more than two states
  # This expression includes concatenation, union, and Kleene star
  expression = 'A.B|C*'
  result = infix2postfix(expression)
  nfa = postRe2NFA(result)
  print(nfa)
  
  
if __name__  ==  '__main__':
  main()