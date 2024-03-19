from Nodo import Nodo
from Grafo import Grafo
from Arco import Arco

file = open('grafoP2.txt')
lines = file.readlines()

G = Grafo('G')
for error,line in enumerate(lines):
    line = line.rstrip()
    linea = line.split(' ')
    if len(linea) == 2 or len(linea) > 3:
        print(f'Error de sintaxis en la linea {error+1} ({linea})')
    elif len(linea) == 3:
        G.addNodo(linea[0])
        G.addNodo(linea[1])
        G.addArco(linea[0],linea[1],linea[2])
    else:
        G.addNodo(linea[0])


print(G)
print(G.mst_bellman_ford('s'))


