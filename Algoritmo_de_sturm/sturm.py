import math

class Rx:
    """Clase para manejo de polinomios de variable real
    """
    def __init__(self, g = -1, c=[]):
        """
        Args:
            g (int, optional): [description]. Defaults to 0.
            *c lista de coeficientes
        """
        self.g = g
        self.c = c.copy()
    
    def __str__(self):
        """

        Returns:
            [str]: resgresa el polinomio en forma de string
        """
        ret = ""
        if self.g<0 or self.g == 0 and self.c[0]==0:
            return "0"
        for i in reversed(range(2,self.g+1)):
            if self.g>=1 and self.c[i]!=0.0:
                if self.c[i]>0:
                    sig = "+"
                else:
                    sig = ""
                ret +="{}{}x^{}".format(sig,round(self.c[i]),i)
        if self.g>=1 and self.c[1]!=0.0: 
                if self.c[1]>0:
                    sig = "+"
                else:
                    sig = ""
                ret +="{}{}x".format(sig,round(self.c[1]))  
        if self.c[0]!=0.0: 
                if self.c[0]>0:
                    sig = "+"
                else:
                    sig = ""
                ret +="{}{}".format(sig,round(self.c[0]))

        return ret
    
    def copy(self):
        return Rx(self.g,self.c)
    
    def copyminus(self):
        return Rx(self.g,list(map(lambda x: -x,self.c)))
        

    
    @classmethod
    def leeRx(cls):
        """ Lee un polinomio
        Returns:
            [RX]:
        """
        g = int(input("Ingrese el grado: "))
        coef = []
        for i in range(g+1):
            coef.append(float(input("x[{}]=".format(i))))

        while coef[g]== 0.0 and g >0: 
            g -= 1
            coef.pop()
        return cls(g,coef)
    
    @staticmethod
    def sum(a, b):
        """Suma de dos polinomios
        Args:
            a (Rx): 
            b (Rx): 
        Returns:
            [Rx]: 
        """
        ret = Rx()
        if a.g<0:   return Rx(b.g,b.c)
        if b.g<0:   return Rx(a.g,a.c)
        
        if a.g<b.g:
            min = a.g;
            ret.g = b.g;
        else:
            min = b.g;
            ret.g = a.g;
        
        for i in range(min+1): ret.c.append(a.c[i]+b.c[i])

        if a.g==min:
            for i in range (min+1,ret.g+1): ret.c.append(b.c[i])
    
        if b.g==min:
            for i in range (min+1,ret.g+1): ret.c.append(a.c[i])

        while ret.c[ret.g]== 0.0 and ret.g >0: 
            ret.g -= 1
            ret.c.pop()
        
        return ret
    
    @staticmethod
    def rest(a, b):
        """Resta de dos polinomios a-b
        Args:
            a (Rx): 
            b (Rx): 
        Returns:
            [Rx]: a-b
        """
        ret = Rx()
        if a.g<0:   return Rx(b.g,b.c)
        if b.g<0:   return Rx(a.g,a.c)
        
        if a.g<b.g:
            min = a.g;
            ret.g = b.g;
        else:
            min = b.g;
            ret.g = a.g;
        
        for i in range(min+1): ret.c.append(a.c[i]-b.c[i])

        if a.g==min:
            for i in range (min+1,ret.g+1): ret.c.append(-b.c[i])
    
        if b.g==min:
            for i in range (min+1,ret.g+1): ret.c.append(a.c[i])

        while ret.c[ret.g]== 0.0 and ret.g >0: 
            ret.g -= 1
            ret.c.pop()
        
        return ret
    
    @staticmethod
    def multMonomio(a, c,  e):
        """ se multiplica un monomio por un numero
        Args:
            a (Rx): [description]
            c (float): [description]
            e (int ): [description]
        Returns:
            [Rx]: 
        """
        ret = Rx()
        ret.g=a.g+e;

        for i in range(ret.g+1): ret.c.append(0.0)
        for i in range(e,ret.g+1): ret.c[i]=a.c[i-e]*c 

        return ret;
    
    @staticmethod
    def esCero(a):
        """Determina si el grado de Rx es negativo
        Args:
            a (Rx):
        Returns:
            [bool]: [
        """
        return a.g<0

    @staticmethod
    def div(a, b):
        """[summary]
        Args: divide dos Rx, a/b
            a (Rx): [description]
            b (Rx): [description]
        Returns:
            [tuple]: (q,r) regresa el cociente y el residuo. a=bq+r
        """
        q = Rx()
        aux = Rx()
        a_aux = Rx()
  
        a_aux= Rx(a.g,a.c)
        
        a=a_aux;


        if a.g<b.g: return q, Rx(a.g,a.c)

        q.g=a.g-b.g
        for i in range(q.g+1): q.c.append(0.0)
        r= Rx(a.g,a.c)
        while not Rx.esCero(r) and (r.g>=b.g):
            grad=a.g-b.g;
            q.c[grad] = a.c[a.g]/b.c[b.g];
            aux = Rx.multMonomio(b, q.c[grad], grad);
            
            a_aux = Rx.rest(a, aux)
            
            a = a_aux;
            r=Rx(a.g,a.c);
        return q, r
    
    def divsintetica(self, c):
        """Realiza divisi´on sintetica

        Args:
            a (Rx): 
            c (float or int): numero a realizar la evaluacion
        Returns:
            [int]:  1 representa que el resto es mayor o igual a cero
                    -1 representa que el resto es menor a cero
        """
        a=self
        d=a.c[a.g]
        for i in reversed(range(1,a.g+1)):
            d=d*c+a.c[i-1]
            if d<=0.0:
                return -1
        return 1
    
    
    def cotasup(self):
        """Determina una cota superior para las raices del polinomio a

        Args:
            a (Rx): 
        Returns:
            [float]: cota superior
        """
        a = self
        g=-1
        i=0.0
    
        while g==-1:
            g=Rx.divsintetica(a,i)
            if g==-1:
                i=i+0.01
        return i
    

    def cotainf(self):
        """Determina una cota inferior para las raices del polinomio 

        Args:
            a (Rx): 

        Returns:
            [float]: cota inferior
        """
        a=self
        b = Rx()
        c = Rx()
 
        g = 0.0
        b.g=a.g
        c.g=a.g
 
        for i in range(a.g+1):
            if i%2 == 0:
                b.c.append(a.c[i])
            else:
                b.c.append(-a.c[i])
        b.c[0]=a.c[0]

        if b.c[a.g]<0.0:
            c = Rx(b.g,list(map(lambda x: -x,b.c)))
        else:
            c = Rx(b.g,b.c)

	    
        return -Rx.cotasup(c)
    
    def deriva(self):
        """Determina la derivada 

        Returns:
            [Rx]: 
        """
        a = self
        p = Rx()
        p.g=a.g-1
        for i in range(a.g):
            p.c.append(a.c[i+1]*(i+1))
        return p;
    
    def ev(self,x):
        """Evalua polinomio
        Args:
            x (float or int): numero a evaluar

        Returns:
            [float]: evaluación
        """
        r=0.0
        for i in reversed(range(1,self.g+1)): 
            r=(r+a.c[i])*x
        r+=self.c[0]
        return r
        


    def algsturm (self):
        """Determina la sucesión de sturm

        Returns:
            [tuple]: (list= sucesión de strurm (Rx), list = tuplas con las raices) tuple(list(Rx),tuple((float,float)))
        """
        a = self
        c = []
        r = Rx()
        j = 0
        roots = []

        #Se determina la sucesión de Sturm
        c.append(a.copy())
        c.append(a.deriva())
  
        for i in range(2,a.g+1):
            r=Rx.div(c[i-2],c[i-1])[1]
            c.append(r.copyminus())

	  
        
        H=a.g;
 
        for i in range(a.g+1):
            if c[i].g<0: H-=1
            else: 
                if c[i].c[c[i].g]==0.0: H-=1
  
        cotaS=a.cotasup()
        cotaI=a.cotainf()

        j=0
        k=0
        # se construye la tabla se signos del algoritmo
        while cotaI<=cotaS :
            paso=0.001;
            while k!=1 and cotaI<=cotaS and ((c[0].ev(cotaI)!=0.0 or c[0].ev(cotaI+paso)!=0.0) and k<=1):
                k=0
                for i in range(H+1):
                    if c[i].ev(cotaI)<0.0 and c[i].ev(cotaI+paso)>0.0: k+=1
                    if c[i].ev(cotaI)>0.0 and c[i].ev(cotaI+paso)<0.0: k+=1
                
                if k==0: cotaI=cotaI+paso
                if k>=2: paso=paso/2.0
            
            if (c[0].ev(cotaI)>=0.0 and c[0].ev(cotaI+paso)<=0.0) or (c[0].ev(cotaI)<=0.0 and c[0].ev(cotaI+paso)>=0.0):
                roots.append((round(cotaI,3),round(cotaI+paso,3)))
                j+=1
            
            cotaI=cotaI+paso
        return c, roots


    
    
    
    
        
        
            

a = Rx.leeRx()
print(a)
s , r= a.algsturm()
print("La sucesión de sturm es:")
for i in range(len(s)):
    print("V{}={}".format(i,s[i]))
if len(r)>0:
    print("\n\nLas raíces están el los siguientes intervalos:")
    for i in range(len(r)):
        print("[{},{}]".format(r[i][0],r[i][1]))
else:
    print("No tiene raíces reales")

    


