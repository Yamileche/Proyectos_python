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
        self.system = ""

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
                        while eq[-1][-1]==" ":
                            eq[-1]==eq[-1][:-1]
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


    def muestra(self, number = 0):
        """Grafica el gráfo donde los nodos rojos son los estoados finales
            azul es el estado inicial y si resulta ser que el estado inicial
            es final éste se pinta de verde
        """
        G = self.automata
        G1 = self.__auxAutom
        alt = 1
        j=0
        # Posiciones de los nodos
        if number == 0:
            pos = nx.circular_layout(G1,scale=1)
            alt = 0.2
            j= 0
        elif number ==1:
            pos = nx.spring_layout(G1, scale = 15, k=50)
            alt = 2
            j = 0
        elif number == 2:
            pos = nx.spectral_layout(G1,scale=5)
        elif number == 3:
            pos = nx.spiral_layout(G1,scale=1, resolution=1, equidistant=True)
            alt = 0.2
        elif number == 4:
            pos = nx.shell_layout(G1, scale = 4)
        elif number == 5:
            pos = nx.planar_layout(G1,scale=5)
            alt = 0.4
        else:
            pos = nx.random_layout(G1)
            alt = 0.05
        
        
        #plt.figure(figsize=(10,10))
        #ax = plt.gca()
        fig, ax = plt.subplots(1, 1, figsize=(15,8))

        # Dibuja las aristas
        for edge in G.edges():
            source, target = edge

            if source == target:  # Relaciones en el mismo punto
                rad = 0.6
                arrowprops = dict(arrowstyle='<-',
                                  color='black',
                                  connectionstyle=f"arc3,rad={rad}",
                                  linestyle='-',
                                  alpha=1,
                                  linewidth=1,
                                  shrinkA=5,
                                  shrinkB=5
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
                                  shrinkA=5,
                                  shrinkB=5
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
                if not (target,source) in G.edges():
                    c = edge
                    rad = 0
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
                    So = tuple(pos[source])
                    Ta = tuple(pos[target])
                    if So[0]-Ta[0] == 0:
                        s = atan(abs(So[1]-Ta[1])/abs(0.000001))
                    else:
                        s = atan(abs(So[1]-Ta[1])/abs(So[0]-Ta[0]))
                    if Ta[0] > So[0] and Ta[1] > So[1]:
                        s += 0
                    elif Ta[0] <= So[0] and Ta[1] > So[1]:
                        s = pi-s
                    elif Ta[0] <= So[0] and Ta[1] <= So[1]:
                        s = s+pi
                    else:
                        s = 2*pi-s
                    thea=s
                    d = sqrt((So[0]-Ta[0])**2+(So[1]-Ta[1])**2)
                    point = (d/2,j)

                    

                    point = (d*cos(thea)/2-j*sin(thea)+So[0],d*sin(thea)/2+j*cos(thea)+So[1])
                    pes = ""
                    pe = len(G.edges[edge]["weight"])
                    for i in range(pe):
                        if i == pe - 1:
                            pes = pes+G.edges[c]["weight"][i]
                        else:
                            pes = pes+G.edges[c]["weight"][i]+", "

                    ax.text(point[0], point[1], pes)

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
        #print(self.SystemEq)

            
            
    def muestra_eq(self):
        """_Muestra las ecuaciones
        """
        if self.system == "":
            self.regularExpresiion()
        return self.system

    
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
        lista = list() # Lista de estados con el inicial primero, los neutrales al inicio y al final los finales
        
        for i in self.initialState:
            lista.append(i)
        for i in self.BStates:
            lista.append(i)
        for i in self.finalstates:
            if  not i in self.initialState:
                lista.append(i)
            
        
        
        
        self.SystemEq.copy() #Copiamos la lista de las ecuaciones padra poder modificarla
        
        rep = dict() # Diccionario con las ecuaciones favtorizadas
        # Factorizar (Se puede optimizar)
        for key, value in  self.SystemEq.items():
            dicc = dict() # Este diccionario va a tener cuantas veces se repite un estado en una ecuación para poderlo factorizar
            for state in value:
                K= True
                for i in range(-1,-len(state)-1,-1):
                    if state[i] == ")" and K:
                        K == False
                        sta = state[i+1:]
                        st = state[1:i]
                        if sta in dicc.keys():
                            dicc.update({sta:dicc[sta]+"+"+st})
                        else:
                            dicc.update({sta:st})
            
            rep.update({key:list(dicc.items())})
        #print(rep)
        SystemEq = dict()
        # La fórmula de Arden se aplica a continuación

        #print(rep)
        for key, value in rep.items():
            w = ""
            for eq in value:
                w += "("+eq[1]+")"+eq[0]+ " + "
            if key in self.finalstates:
                w += "empty + "
            w = w[:-3]

            if key in w:
                if self.aux3(w) == 1 or (self.aux3(w) == 2 and "empty" in w):
                    n = w.rfind(")")
                    if "*" in i:
                        m = i.rfind("*")
                        n = max([m,n])
                    w = w[:n+1]+"*"
                else:
                    DF = w.split(" + ")
                    for i in DF:
                        if key in i:
                            n = i.rfind(")")
                            if "*" in i:
                                m = i.rfind("*")
                                n = max([m,n])
                            D = i[:n+1]+"*"
                    w = ""
                    for i in DF:
                        if not key in i and i != "empty":
                            w += D+i + " + "
                    if "empty" in DF:
                        w+= D
                    else:
                        w=w[:-3] 
                      
            SystemEq.update({key:w})
       
        

        
        
        # Determina el string del sistema de ecuaciones
        system = ""
        for key, value in SystemEq.items():
            system += key + "="+value+"\n"
        self.system = system
        
        
        for i in self.initialState:
            Ini = i
        #print(SystemEq)
        lista.reverse()
        for i in lista:
            #print("\n"+i)
            self.aux1(SystemEq, i)
            #print(SystemEq)
           
        #print("\n\nFinal:  "+SystemEq["q0"])
        return SystemEq[Ini]
            
            
      
  
    def aux3(self, word=""):
        n=0
        
        n+=word.count(" + ")
        n+=1
        return n 
            
    def aux1(self,SystemEq = dict(), state = ""):
        """Sustituye el estado state en todas las ecuaciones
        """
        aux = dict()
        aux2 = SystemEq.copy()
        #Sutituye
        for key, value in SystemEq.items():
            if state in value:
                if self.aux3(value)>1:
                    Asus = value.split(" + ")
                    w=""
                    K = aux2[state]
                    if self.aux3(K)>1:
                        PorS = K.split(" + ")
                        for word in Asus:
                            if state in word:
                                for k in PorS:
                                    if k!="empty":
                                        w+=word[0:word.find(state)]+k+" + "
                                    else:
                                        w+=word[0:word.find(state)]+" + "            
                            else:
                                w+=word+" + "
                    else:
                       for word in Asus:
                            if state in word:
                                w+=word[0:word.find(state)]+K+" + "
                            else:
                                w+=word+" + "
                    w=w[0:-3]
                else: 
                    K = aux2[state]
                    Asus = value
                    w=""
                    if self.aux3(K)>1:
                        PorS = K.split(" + ")
                        for k in PorS:
                            if k =="empty":
                                w+=Asus[0:Asus.find(state)]+" + "
                            else:
                                w+=Asus[0:Asus.find(state)]+k+" + "
                    else:
                       w+=Asus[0:Asus.find(state)]+K+" + "
                    w=w[0:-3]
                aux2.update({key:w})
        aux = aux2.copy()
        
        #print("\n")
        #print(aux)

        #Factorización
        for key, value in aux.items():
            if self.aux3(value)>1:
                dicc = dict()
                Asus = value.split(" + ")
                l=False
                if "empty" in Asus:
                    l=True
                statecount=dict()
                for i in Asus:
                    if i != "empty":
                        n = i.rfind(")")
                        m = 0
                        if "*" in i:
                            m = i.rfind("*")
                            n = max([m,n])
                        estado = i[n+1:]
                        if estado in dicc.keys():
                            dicc.update({estado:dicc[estado]+"+"+i[:n+1]})
                            statecount.update({estado:statecount[estado]+1})
                        else:
                            dicc.update({estado:i[:n+1]})
                            statecount.update({estado:1})
                final = ""
                for Key, Value in dicc.items():
                    if statecount[Key]>1:
                        final+="("+Value+")"+Key+" + "
                    else:
                        final+=Value+Key+" + "
                        
                if l:
                    final+="empty + "
                final = final[:-3]
                aux2.update({key:final})
        
        #print("\n")
        #print(SystemEq)
        
        # Arden
        aux = aux2.copy()
        for key, value in aux.items():
            final = ""
            if key in value:
                if self.aux3(value) == 1:
                    n = value.rfind(")")
                    m = 0
                    if "*" in value:
                        m = value.rfind("*")
                        n = max([m,n])
                    final = "("+value[:n+1]+")*"+ " + "
                else:
                    Asus = value.split(" + ")
                    for word in Asus:
                        if key in word:
                            n = word.rfind(")")
                            m = 0
                            if "*" in word:
                                m = word.rfind("*")
                                n = max([m,n])
                            final = "("+word[:n+1]+")*"
                            
                    if not (len(Asus) == 2 and ("empty" == Asus[0] or "empty" == Asus[1])):
                        extra=""
                        for word in Asus:
                            if not key in word:
                                if word != "empty":
                                    extra += final+word+" + "
                                else:
                                    extra+=final+ " + "
                        final = extra[:-3]
            else:
                final = value        
            aux2.update({key:final})
        SystemEq.update(aux2)
        #print("\n")
        #print(SystemEq)
        
        
    def aux2(self, SystemEq= dict()):
            for i in self.initialState:
                Ini = i
            eq = SystemEq[Ini]
            for i in self.automata.nodes:
                if i in eq:
                    return True
            return False



"""
autom1 = automata()
autom1.leestados(
    r"direccion_del_archivo/archivo.txt")
print("La expresión regular es: ")
print(autom1.regularExpresiion())

print("\n\nEl sistema de ecuaciones es: ")
print(autom1.muestra_eq())

if autom1.acepta("1 0 1 0 1 0 0 1"):
    print("\n\nLa palabra es aceptada")
else:
    print("\n\nLa palabra no es aceptada")

print("\n\n")
# Posiciones del 0 al 6
autom1.muestra(number=1)
"""