from decimal import Decimal
import networkx as nx
import matplotlib.pyplot as plt
from math import sqrt, atan, sin, cos, pi


def rotate(source=(0, 0), target=(0, 0), rad=1):
    """_summary_

    Args:
        source (tuple, optional): _description_. Defaults to (0, 0).
        target (tuple, optional): _description_. Defaults to (0, 0).
        rad (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """
    # Determina la altitud del peso

    c = sqrt((source[0]-target[0])** 2+(source[1]-target[1])**2)
    B = ((pi)-rad)/2
    r =  ( (sin(B))*c)/ (sin(rad))
    k =  (sqrt(r**2- ((c/2)**2)))
    l =  ( (r)- (k))
    c = (c/2, 2*l+c/20)

    # Determinar el ángulo a rotar
    if source[0]-target[0] == 0:
        s = atan(abs(source[1]-target[1])/abs(0.000001))
    else:
        s = atan(abs(source[1]-target[1])/abs(source[0]-target[0]))
    if target[0] > source[0] and target[1] > source[1]:
        s += 0
    elif target[0] <= source[0] and target[1] > source[1]:
        s = pi-s
    elif target[0] <= source[0] and target[1] <= source[1]:
        s = s+pi
    else:
        s = 2*pi-s

    x =  (c[0])
    y =  (c[1])
    z =  (cos(s))
    w =  (sin(s))
    c = (x*z-y*w, x*w+y*z)
    c = (float(c[0])+source[0], float(c[1])+source[1])
    return c


class automata:
    def __init__(self, state=[], regex=""):
        self.state = state
        self.regex = regex
        self.eq = dict()
        self.automata = nx.DiGraph()
        self.isfinal = dict()
        self.finalstates = set()
        self.initialState = set()
        self.BStates = set()
        self.alphabet = list()
        self.SystemEq = dict()
        self.__auxAutom = nx.DiGraph()

    def leestados(self, archivo=""):
        """Lee los estados y acomoda la información

        Args:
            archivo (str, optional): _dirección del archivo txt a leer_. Defaults to "".
        """
        if self.state == []:
            f = open(archivo)
            states = []
            statesAux = []
            lines = f.readlines()
            num = len(lines)
            l = 1

            eq = lines[0].split(" ")
            if eq[-1].find("\n") != -1:
                eq[-1] = eq[-1][:-1]

            self.alphabet = eq   #Obteniendo el alfabeto

            k = False
            while l < num:
                eq = lines[l].split(" ")
                if eq[-1].find("\n") != -1:
                    eq[-1] = eq[-1][:-1]

                if k:  # Se añaden las relaciones entre los estados
                    h = False  # la arista con el peso no está agregada
                    for i in states:
                        # Si la arista se encuentra en la lista de aristas
                        if eq[0] == i[0] and eq[1] == i[1]:
                            h = True  # Se coloca aquí en caso de que esté la arista
                            if not eq[2] in i[2]:  # Si no está el peso se agrega
                                i[2].append(eq[2])
                                

                    if not h:  # Si aún no se agrega la arista con el peso
                        statesAux.append(tuple(eq))
                        eq[2] = [eq[2]]
                        states.append(tuple(eq))
                    l += 1

                if not k:  # Se añaden los estados y si son finales, etc...
                    l += 1
                    k = True
                    n = int(eq[0])
                    for i in range(n):
                        eq1 = lines[l].split(" ")
                        if eq1[-1].find("\n") != -1:
                            eq1[-1] = eq1[-1][:-1]
                        if int(eq1[1]) == 1:  # Final
                            self.isfinal.setdefault(eq1[0], True)
                        elif int(eq1[1]) == 2:
                            # Inicial y final
                            self.isfinal.setdefault(eq1[0], True)
                            self.initialState = self.initialState.union([
                                                                        eq1[0]])
                        else:  # Inicial
                            if int(eq1[1]) == -1:
                                self.initialState = self.initialState.union([
                                                                            eq1[0]])
                            self.isfinal.setdefault(eq1[0], False)
                        l += 1
            for key, value in self.isfinal.items():
                if value:
                    self.finalstates = self.finalstates.union(set([key]))
            self.automata.add_weighted_edges_from(states)
            self.__auxAutom.add_weighted_edges_from(statesAux)
            self.state = states 
            self.BStates = set(self.automata.nodes).difference(self.finalstates.union(self.initialState)) #Nodos que no son finales ni iniciales


    def muestra(self):
        """Grafica el gráfo donde los nodos rojos son los estoados finales
            azul es el estado inicial y si resulta ser que el estado inicial
            es final éste se pinta de verde
        """
        G = self.automata
        G1 = self.__auxAutom
        # Posiciones de los nodos

        #pos = nx.circular_layout(G1)
        pos = nx.spring_layout(G1)
        #pos = nx.spectral_layout(G1)
        #pos = nx.spiral_layout(G1)
        #pos = nx.shell_layout(G1)
        
        #pos = nx.planar_layout(G1)
        #pos = nx.random_layout(G1)
        
        
        #plt.figure(figsize=(10,10))
        #ax = plt.gca()
        fig, ax = plt.subplots(1, 1, figsize=(5,5))

        # Dibuja las aristas
        for edge in G.edges():
            source, target = edge

            if source == target:  # Relaciones en el mismo punto
                rad = 0.6
                alt = 0.2
                arrowprops = dict(arrowstyle='<-',
                                  color='black',
                                  connectionstyle=f"arc3,rad={rad}",
                                  linestyle='-',
                                  alpha=1,
                                  linewidth=1,
                                  shrinkA=10,
                                  shrinkB=10
                                  )
                rot = pos[source].copy()
                rot[1] = rot[1] + alt

                ax.annotate("",
                            xy=pos[source],
                            xytext=rot,
                            #textcoords='offset points',
                            arrowprops=arrowprops
                            )
                arrowprops = dict(arrowstyle='->',
                                  color='black',
                                  connectionstyle=f"arc3,rad={-rad}",
                                  linestyle='-',
                                  alpha=1,
                                  linewidth=1,
                                  shrinkA=10,
                                  shrinkB=10
                                  )
                ax.annotate("",
                            xy=pos[source],
                            xytext=rot,
                            #textcoords='offset points',
                            arrowprops=arrowprops
                            )
                pes = ""
                pe = len(G.edges[edge]["weight"])
                for i in range(pe):
                    if i == pe - 1:
                        pes = pes+G.edges[edge]["weight"][i]
                    else:
                        pes = pes+G.edges[edge]["weight"][i]+", "
                ax.text(pos[source][0], pos[source][1]+alt, pes)

            else:
                rad = 0.2
                c = edge
                arrowprops = dict(arrowstyle='<-',
                                  color='black',
                                  connectionstyle=f"arc3,rad={rad}",
                                  linestyle='-',
                                  alpha=1,
                                  linewidth=1,
                                  shrinkA=10,
                                  shrinkB=10
                                  )
                ax.annotate("",
                            xy=pos[source],
                            xytext=pos[target],

                            #textcoords='offset points',
                            arrowprops=arrowprops
                            )

                s = rotate(tuple(pos[source]), tuple(pos[target]), rad)
                pes = ""
                pe = len(G.edges[edge]["weight"])
                for i in range(pe):
                    if i == pe - 1:
                        pes = pes+G.edges[c]["weight"][i]
                    else:
                        pes = pes+G.edges[c]["weight"][i]+", "

                ax.text(s[0], s[1], pes)

        # Dibuja los nodos
        nx.draw_networkx_nodes(G, pos, nodelist=list(self.finalstates),
                               node_color="red")
        if self.finalstates.intersection(self.initialState) == set():
            nx.draw_networkx_nodes(G, pos, nodelist=list(self.initialState),
                                   node_color="blue")
        else:
            nx.draw_networkx_nodes(G, pos, nodelist=list(self.initialState),
                                   node_color="green")
        nx.draw_networkx_nodes(G, pos, nodelist=list(set(G.nodes).difference(self.finalstates.union(self.initialState))),
                               node_color="black")
        # labels
        nx.draw_networkx_labels(G, pos,
                                font_family="sans-serif",
                                font_color='white')

        plt.box(False)
        plt.show()

    def __equations(self):
        """Determina las ecuaciones del autómata
        """
        for node in self.automata.nodes:
            lista = []
            for i in self.state:
                if node == i[0]:
                    for weight in i[2]:
                        lista.append((i[1],weight))
            self.eq.setdefault(node,lista)

        for key, value in self.eq.items():  # Por si hay nodos que no tienen sucesores se pone por   
            auxlist2 = list()               # defecto ellos mismos como sucesores para cualquier
            if value == list():             # letra del alfabeto
                auxlist = dict()  
                auxlist3 = list()  #Aquí se guardan las tuplas
                for i in self.alphabet:
                    auxlist3.append((key,i))
                auxlist.update({key:auxlist3})
                
                auxlist2.append(auxlist.copy())
        
        if auxlist2 != list():
            for i in auxlist2:
                self.eq.update(i)  


        for key, value in self.eq.items(): # Se crea un diccionario con los strings de las ecuaciones
            k = len(value)
            l = ""
            for i in range(k):
                s = "("+ str(value[i][1])+")" + str(value[i][0]+" ")
                l += s 
            self.SystemEq.update({key:l.split(" ")[0:-1]})

            
            
    def muestra_eq(self):
        """_Muestra las ecuaciones
        """
        if self.eq == dict():
            self.__equations()
        print("\nEl sistema de ecuaciones es: \n")
        for key, value in self.eq.items():
            print(key,end="=")
            k = len(value)
            for i in range(k):
                s = "("+ str(value[i][1])+")" + str(value[i][0])
  
                if i == k-1:
                    print(s)
                else:
                    print(s+"+",end="")

    
    def acepta(self,word = ""):
        if self.eq == dict():
            self.__equations()
        word = word.split(" ")
        
        for node in self.initialState: #Tuve que poner bucle para poder obtener el punico elemento en el conjunto
            EsIn = node
        if self.eq[EsIn] == []: # No tiene conexiones con otros nodos
            return False
        
        n=0
        
        if len(word) == 1:
            if EsIn in self.finalstates:
                if (EsIn,word[0]) in self.eq[EsIn]:
                    return True
            return False
        
        letra = word[n]
        
        for tup in  self.eq[EsIn]:
            if tup[1] == letra: # Recorre cada conexion para ver si es aceptado
                if self.cambiaEstado(tup[0],word,n):
                    return True
        
        return False
        
    
    def cambiaEstado(self, nextState="", word = "", n = 0):
        if n + 1 == len(word): #Final de la palabra
            if nextState in self.finalstates: #Si está en u estado de aceptación
                return True
            return False    #Si no está en un estado de aceptación
        
        
        #En caso de que no nos encontremos en el último caracter
        if self.eq[nextState] == []: # No tiene conexiones con otros nodos
            return False
        
        n+=1
        letra = word[n]
        for tup in  self.eq[nextState]:
            if tup[1] == letra: # Recorre cada conexion para ver si es aceptado
                if self.cambiaEstado(tup[0],word,n):
                    return True
        
        return False
    
    def regularExpresiion(self):
        if self.eq == dict():
            self.__equations()
        G = self.automata
        st = [] #Esta lista contiene los estados en orden: inicial, normal, final
        for i in self.initialState:
            st.append(i)
        for i in self.BStates:
            st.append(i)
        for i in self.finalstates.difference(self.initialState):
            st.append(i)
        print(self.SystemEq)

        
        


autom1 = automata()
autom1.leestados(
    r"/home/yamilongo/Documentos/OneDrive/Documentos/GitHub/Proyectos_python/ArchComp/autom1.txt")
#autom1.muestra_eq()
autom1.regularExpresiion()
#if autom1.acepta("0 0 0 0 0 0 1 1 0 1"):
#    print("La palabra es aceptada")
#else:
#    print("La palabra no es aceptada")
#autom1.regularExpresiion()
#autom1.muestra()