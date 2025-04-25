import re


def infix2postfix(regex):
  postFix = []
  stack = []
  precedence = {
    '^' : 5,
    '/': 4,
    '*': 4,
    '+': 3,
    '-' : 3,
    '(': 1
  }
  
  associativity = {
    'RL': '^',
    'LR': '*/+-'
  }
  
  for ele in regex:
    if ele not in "()^/*+-":
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
            lastEle = stack.pop()
            postFix.append(lastEle)
        stack.append(ele)
      
      elif precedence[ele] == precedence[stack[-1]]:
        if ele in associativity['RL']:
          stack.append(ele)
        elif ele in associativity['LR']:
          sameLastAsso = stack.pop()
          postFix.append(sameLastAsso)
          stack.append(ele)
    else:
      stack.append(ele)
  
  while len(stack) > 0:
    lastStackEle = stack.pop()
    postFix.append(lastStackEle)
  
  postFix = ''.join(postFix)
  noBlanks = postFix.replace(" ", "")
  #print(noBlanks)
  return noBlanks
    
def postRe2NFA(postfix):
  #waits for postfix re
  regex=''.join(postfix)

  #abecedario, takes only the elements it sees in the expression 
  keys=list(set(re.sub('[^A-Za-z0-9]+', '', regex)+'e'))

  s=[]
  stack=[]
  start=0
  end=1
  
  #counter for states
  counter=-1 
  
  #classifier for the different states we will have
  c1=0 
  c2=0

  for i in regex:
      if i in keys:
          counter=counter+1
          c1=counter
          counter=counter+1
          c2=counter
          s.append({})
          s.append({})
          stack.append([c1,c2])
          s[c1][i]=c2
      elif i=='*':
          r1,r2=stack.pop()
          counter=counter+1
          c1=counter
          counter=counter+1
          c2=counter
          s.append({})
          s.append({})
          stack.append([c1,c2])
          s[r2]['e']=(r1,c2)
          s[c1]['e']=(r1,c2)
          if start==r1:start=c1 
          if end==r2:end=c2 
      elif i=='.' or i == '?':
          r11,r12=stack.pop()
          r21,r22=stack.pop()
          stack.append([r21,r12])
          s[r22]['e']=r11
          if start==r11:start=r21 
          if end==r22:end=r12 
      else:
          counter=counter+1
          c1=counter
          counter=counter+1
          c2=counter
          s.append({})
          s.append({})
          r11,r12=stack.pop()
          r21,r22=stack.pop()
          stack.append([c1,c2])
          s[c1]['e']=(r21,r11)
          s[r12]['e']=c2
          s[r22]['e']=c2
          if start==r11 or start==r21:start=c1 
          if end==r22 or end==r12:end=c2
  print (keys)
  print (s)
  
  
def main():
  re1 = infix2postfix('A * B + C * D') # Expected: AB*CD*+
  #re2 = infix2postfix('A + B * (C + D)')  # Expected: ABCD+*+
  postRe2NFA(re1)
  
  
if __name__ == '__main__':
  main()