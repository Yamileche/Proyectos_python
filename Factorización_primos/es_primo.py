class Integer():
    """Clase para estructura de números enteros
    """

    def __init__(self):
        """Constructor

        Args:
            p (list, optional): [factorización del primo]. Defaults to [].
            d (list, optional): [potencial del número primo en la descomposición prima]. Defaults to [].
            s (int, optional): [description]. Defaults to 1.
        """
        self.p = []
        self.d = []
        self.s = 1
        self.phi = 1
        self.mcd = 1
        self.mcm = 1



def primo(k=1):
    p = Integer()
    r = Integer()
    s = 0
    w = k
    f = 0
    g = 0

    if k >= 2:
        p.p.append(2)
        s += 1
    if k >= 3:
        p.p.append(3)
        s += 1
    if k >= 5:
        p.p.append(5)
        s += 1
    if k >= 7:
        p.p.append(7)
        s += 1
    if k >= 11:
        p.p.append(11)
        s += 1
    if k >= 13:
        p.p.append(13)
        s += 1
    if k >= 17:
        p.p.append(17)
        s += 1
    if k >= 19:
        p.p.append(19)
        s += 1
    if k >= 23:
        p.p.append(19)
        s += 1

    for i in range(4, k):
        t = 6*i+1
        for j in range(s):
            if t % p.p[j] != 0 or (t+4) % p.p[j] != 0:
                if t % p.p[j] != 0 and k % t == 0:
                    f = 1
                if (t+4) % p.p[j] != 0 and k % (t+4) == 0:
                    g = 1
        if f == 1:
            p.p.append(t)
            s += 1

        if g == 1:
            p.p.append(t+4)
            s += 1
        g = 0
        f = 0
        if 6*i+1.0 > k+0.0: break

    p.s = s
    r.s = s
    for i in range(s):
        r.p.append(p.p[i])

    p = Integer()
    l = 0;
    for i in range(s):
        r.d.append(0)
        if w % r.p[i] == 0 and w > 0:
            l += 1
        for j in range(s):
            if w % r.p[i] == 0 and w > 0:
                w = w/r.p[i]
                r.d[i] = r.d[i]+1

    w = 0
    for i in range(s):
    	if r.d[i] != 0:
            p.p.append(r.p[i])
            p.d.append(r.d[i])
            w += 1

    p.s = l

    p.phi = 1

    for i in range(p.s):
        p.phi *= (p.p[i]-1)
        if p.d[i] != 1: p.phi *= p.p[i]**(p.d[i]-1)
    return p


def factorizacion(k=0):
	r = primo(k)
	print("\n{}=".format(k), end="")
	for i in range(r.s):
		if r.d[i] != 0:
			if r.d[i] != 1: print("({}^{})".format(r.p[i], r.d[i]), end="")
			else: print("({})".format(r.p[i]), end="")

			
		






def mcd(n = 1,m = 1):

    t = Integer()
    l=0
    w=0
    u=1
    r=primo(m)
    p=primo(n)
	
    mcd = 1
    for i in range(r.s):
        for j in range(p.s):
            if r.p[i]==p.p[j]: 
                l+=1
    
    t.s=l;

    for i in range(r.s):
        for j in range(p.s):
            if r.p[i]==p.p[j]:
                t.p.append(r.p[i])
                if r.d[i]<p.d[j]: t.d.append(r.d[i])
                else: t.d.append(p.d[j])
                w+=1
			
		
    
    mcd = 1

    for i in range(l):
        if r.d[i]!=0 :
            mcd *= (t.p[i]**t.d[i])
    p.mcd=m
    mcm = int((n * m)/mcd)
    print(mcd)
    print("\nmcm({}, {})=".format(m,n), end="")
    print(mcm)
    p.mcd=mcm

print(785421548651)
factorizacion(785421548651)
factorizacion(875)
mcd(1500,875)


