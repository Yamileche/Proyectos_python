from copy import deepcopy
import time
from math import sqrt
import sys
sys.setrecursionlimit(300000)
global size, Bool
size = 200
Bool = False


x = 1
y = 1

tablero = list()
row = list()
for i in range(size):
    row.append(0)
for i in range(size):
    tablero.append(row.copy())
    
x-=1
y-=1
tablero[y][x] = 1


solutions = list()
    
def muestra(tab = list()):
    if tab == list():
        return None
    for i in range(size):
        for j in range(size):
            print(str(tab[i][j]).ljust(len(str(size*size))), end = "  ")
        print()
        
        
def nextPos(pos = list(), tab = tablero):
    hor = pos[0]
    ver = pos[1]
    return sorted([[hor+i, ver+j] for i in [-2, 2, 1, -1] for j in [-1, 1, 2, -2] if abs(i)!=abs(j) and hor+i >=0 and hor+i<size and ver+j>=0 and ver+j<size and tab[ver+j][hor+i] == 0])


def filtrado(tab = tablero):
    
 
    count = 0

    for i in range(size):
        for j in range(size):
            if tab[j][i] == 0:
                next = nextPos(pos = [i,j], tab = tab)
                T = False
                for k in next:
                    if tab[k[1]][k[0]] == 0:
                        T = True
                if not T:
                    count+=1
                if count >2:
                    #print("\nsolo\n")
                    #muestra(tab)
                    return False
                    
                
    return True

def siguiente(tab = tablero, pos = [0,0]):
    next = nextPos(pos)
    next = sorted(next, key= lambda x: len(nextPos(pos = x, tab=tab)))
    m = len(next)
    if m>1:
        l = len(nextPos(pos = next[0], tab=tab))
        n = m
        for k in range(m):
            if l < len(nextPos(pos=next[k],  tab=tab)):
                n= k
                break
        nextAux = next[:n]
        #nextAux = sorted(nextAux, key= lambda x: min([x[0] + x[1],2*size - x[0] - x[1]]))
        nextAux = sorted(nextAux, key= lambda x: min(
                            [x[0]**2+x[1]**2,(x[0]-size-1)**2+x[1]**2,
                            x[0]**2+(x[1]-size-1)**2,
                            (x[0]-size-1)**2+(x[1]-size-1)**2]
                            )
                        )
        for k in range(n):
            next[k] = nextAux[k]

    return next
            
                
def control(tab = tablero, pos = [0,0], num = 2):
    global Bool
    if num > size*size or Bool or not filtrado(tab = tab):
        return None
    

    next = siguiente(pos = pos, tab = tab)
    
    #print("\n\n Cambio", next)
    #print("\n\nEntra")
    if len(next) > 0:
        for i in next:
            #print("\n\n", i, pos)
            if Bool:
                break
            if tab[i[1]][i[0]] != 0:
                #print("\n\nNo pas??")
                continue

            tabaux = deepcopy(tab)
            tabaux[i[1]][i[0]] = num
            #print("\n\n", num, next)
            #muestra(tabaux)
            if num == size*size:
                Bool = True
                #print("lleg??")
                tablero = tabaux
                solutions.append(deepcopy(tabaux))
                return None
            control(tab = tabaux, pos = i, num = num+1)

    #print("\nVac??o")


print("\nEsto puede tardar...\n\n")
inicio = time.time() 
muestra(tablero)

control(pos = [x,y])
print(siguiente(pos=[x,y]))
print("\n\n\nSoluci??n:\n")
if solutions != list():
    muestra(solutions[0])
final = time.time()
print("\n\nTiempo de ejecuci??n: ", final-inicio, "s")
