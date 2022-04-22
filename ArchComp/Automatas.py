import networkx as nx
import matplotlib.pyplot as plt
from math import sqrt, atan, sin, cos,pi

input("Ingrese el número")

def rotate(source=(0,0),target=(0,0)):
    lenght=sqrt((source[0]-target[0])**2+(source[1]-target[1])**2)
    l=lenght/15
    c=(lenght/2,l)
    
    #Determinar el ángulo a rotar
    s=atan(abs(source[1]-target[1])/abs(source[0]-target[0]))
    if target[0]>source[0] and target[1]>source[1]:
        s+=0
    elif  target[0]<=source[0] and target[1]>source[1]:
        s=pi-s
    elif target[0]<=source[0] and target[1]<=source[1]:
        s=s+pi
    else:
        s=2*pi-s
        
    x=c[0]
    y=c[1]
    z=cos(s)
    w=sin(s)
    c=(x*z-y*w,x*w+y*z)
    c=(c[0]+source[0],c[1]+source[1])
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
        

    def leestados(self, archivo=""):
        """Lee los estados y acomoda la información

        Args:
            archivo (str, optional): _dirección del archivo txt a leer_. Defaults to "".
        """
        if self.state == []:
            f = open(archivo)
            states = []
            lines=f.readlines()
            num=len(lines)
            l=0
            k = False
            while l<num:
                eq = lines[l].split(" ")
                if eq[-1].find("\n") != -1:
                    eq[-1] = eq[-1][:-1]
                if k:
                    states.append(tuple(eq))
                    l+=1
                if not k:
                    l+=1
                    k=True
                    n = int(eq[0])
                    for i in range(n):
                        eq1 = lines[l].split(" ")
                        if eq1[-1].find("\n") != -1:
                            eq1[-1] = eq1[-1][:-1]
                        if int(eq1[1])==1:
                            self.isfinal.setdefault(eq1[0],True)
                        else:
                           if int(eq1[1]) == -1:
                                self.initialState = self.initialState.union([eq1[0]]) 
                           self.isfinal.setdefault(eq1[0],False) 
                        l+=1
            for key,value in self.isfinal.items():
                if value:
                    self.finalstates = self.finalstates.union(set([key]))        
            self.automata.add_weighted_edges_from(states)

    def muestra(self):
        """Grafica el gráfo donde los nodos rojos son los estoados finales
        """
        G = self.automata
        """""
        pos = nx.spring_layout(G)
        #pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True,nodelist=list(self.finalstates),
                node_color="red", font_color="white")
        nx.draw(G, pos, with_labels=True,nodelist=list(self.initialState),
                node_color="blue", font_color="white")
        nx.draw(G, pos, with_labels=True,nodelist=list(set(G.nodes).difference(self.finalstates.union(self.initialState))),
                node_color="black", font_color="white")
        
        labels = nx.get_edge_attributes(G, 'weight')
        
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=labels, label_pos=0.3, font_size=15)
       
        #ax = plt.gca()
        #for edge in G.edges():
        #    source, target = edge
        #    rad = 0.2
        #    c = edge
        #    arrowprops=dict(arrowstyle="-", 
        #            color='black' if c else 'blue',
        #            connectionstyle=f"arc3,rad={rad}",
        #            linestyle= '-' if c else '--',
        #            linewidth=1)
        #    ax.annotate("",
        #            xy=pos[source],
        #             xytext=pos[target],
        #            arrowprops=arrowprops
        #            )   
        """
        """"""

        #
        #pos = nx.circular_layout(G)

        pos = nx.spring_layout(G)

        ax = plt.gca()

        for edge in G.edges():
            source, target = edge
            rad = 0.2
            c = edge
            arrowprops=dict(arrowstyle='<-', 
                            color='black' ,
                            connectionstyle=f"arc3,rad={rad}",
                            linestyle= '-',
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
            
            s=rotate(tuple(pos[source]),tuple(pos[target]))
            ax.text(s[0],s[1],G.edges[c]["weight"])
            rotate(source= tuple(pos[source]),target= tuple(pos[target]))
        # nodes

        nx.draw_networkx_nodes(G, pos,nodelist=list(self.finalstates),
                node_color="red")
        nx.draw_networkx_nodes(G,pos, nodelist=list(self.initialState),
                node_color="blue")
        nx.draw_networkx_nodes(G,pos, nodelist=list(set(G.nodes).difference(self.finalstates.union(self.initialState))),
                node_color="black")
        # labels
        nx.draw_networkx_labels(G, pos, 
                                font_family="sans-serif", 
                                font_color ='white')
        

        plt.box(False)
        plt.show()
    
    def equations(self):
        for edges in self.automata.edges:
            self.automata
        


autom1 = automata()
autom1.leestados(r"ArchComp\autom1.txt")
autom1.muestra()