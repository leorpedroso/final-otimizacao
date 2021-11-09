import os
import re
filepath_rm = os.path.join('/home/leo/Documents/2021_1/Otimizacao/Trabalho/final-otimizacao/rm','RM12')
filepath_ans = os.path.join('/home/leo/Documents/2021_1/Otimizacao/Trabalho/final-otimizacao','answer_12.txt')

chars = "x[](),\n"

def open_rm():
  edges = []
  with open(filepath_rm) as f:
    line = f.readline()
    line = f.readline()
    line = f.readline()
    line = f.readline()

    for line in f:
      l = line
      l = re.sub('[x[](),]', '', l)
      l = re.sub('\n', '', l)
      l = " ".join(l.split()).split(' ')
      edges.append(l)
  
  return edges

def open_ans():
  edges = []
  with open(filepath_ans) as f:
    for line in f:
      l = line
      for c in chars:
        l = l.replace(c, "")
      l = l.split(' ')
      edges.append(l)
  
  return edges

def correct_answer(rm, ans):
  edges = []
  ks = []

  if len(rm) != len(ans):
    return False

  for i in range(len(ans)):
    if ans[i][0] == '1.0':
      edges.append(rm[i][0])
      edges.append(rm[i][1])
      ks.append(rm[i][2])

  if len(edges) != len(set(edges)):
    return False

  if len(ks) != len(set(ks)):
    return False
  
  return True

rm = open_rm()
ans = open_ans()

if correct_answer(rm, ans):
  print('OK')
else:
  print('Errado')
#print(ans)


