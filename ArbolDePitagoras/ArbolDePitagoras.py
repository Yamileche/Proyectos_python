import matplotlib.pyplot as plt
import numpy as np
from bokeh.palettes import Magma, Inferno, Plasma, Viridis, Cividis 
import seaborn as sns
from math import cos, sin, pi, asin, acos, sqrt


global al, theta, gamma, a, l, h, ce, cosg, seng, cost, sent, n, alpha

l = 1
h = 1
a = 0.3
#a = 1/(2*sin(pi/4)) #arbol normal ramas simétricas
grad = 90 # ángulo en grados

n=3 # Recursiones

# Paletas de Seaborn
paleta = sns.color_palette("cividis", n_colors=n+1) 


#Listado de paletas
# 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 
# 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2 ',' Dark2_r ',' GnBu ',' GnBu_r ','
# Verdes ',' Verdes_r ',' Grises ',' Grises_r ',' OrRd ',' OrRd_r ',' Naranjas ',' Naranjas_r ',
# ' PRGn ', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 
# 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r ',' PuOr ',' PuOr_r ',' PuRd ',' PuRd_r ','
# Purples ',' Purples_r ',' RdBu ',' RdBu_r ',' RdGy ',' RdGy_r ',' RdPu ',' RdPu_r ', 'RdYlBu', 
# 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 
# 'Set3_r', 'Spectral ',' Spectral_r ',' Wistia ',' Wistia_r ',' YlGn ',' YlGnBu ',' YlGnBu_r ',' YlGn_r ',
# ' YlOrBr ',' YlOrBr_r ',' YlOrRd ',' YlOrRd_hotr ', 'afmhot_r', 'otoño', 'otoño_r', 'binario', 'binario_r', 
# 'hueso', 'hueso_r', 'brg', 'brg_r', 'bwr','bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 
# 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r ',' gist_earth ',
# ' gist_earth_r ',' gist_gray ',' gist_gray_r ',' gist_heat ',' gist_heat_r ',' gist_ncar ',
# ' gist_ncar_r ',' gist_rainbow ',' gist_rainbow_r ',' gist_stern_stern 'gist_yarg', 'gist_yarg_r', 
# 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 
# 'icefire ',' icefire_r ',' inferno ',' inferno_r ',' jet ',' jet_r ',' magma ',' magma_r ',' mako ',
# ' mako_r ',' nipy_spectral ',' nipy_spectral_r ',' océano ', 'ocean_r', 'pink', 'pink_r', 'plasma', 
# 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'sismic', 'seismic_r ',
# ' primavera ',' primavera_r ',' verano ',' verano_r ',' tab10 ',' tab10_r ',' tab20 ′, 'tab20_r', 
# 'tab20b', 'tab20b_r','tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 
# 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag ',' vlag_r ',
# ' invierno ',' invierno_r '





"No mover lo que sigue"


alpha = 1

al = grad * pi/ 180

#al = acos(1-1/(2*a*a))

theta = asin(sin(al)*a)
gamma = pi - theta - al

cosg = cos(gamma)
seng = sin(gamma)
cost = cos(theta)
sent = sin(theta)
Cost = cos(-theta)
Sent = sin(-theta) 
MaxV = [h]
MinV = [0]
MaxH = [l]
MinH = [0]
ce = (seng/sin(al))

def f2 (w = [0,0]):
    x = w[0]
    y = w[1]
    return [a*x*cosg-a*y*seng, a*x*seng+a*y*cosg+h]
 
def f3 (w = [0,0]):
    x = w[0]
    y = w[1]
    #return [-ce*x*cost+ce*y*sent+l, ce*x*sent+ce*y*cost+h]
    
    return [x*ce*Cost-y*ce*Sent+a*cosg ,x*ce*Sent+y*ce*Cost+a*seng +h]

# Paletas  Magma, Inferno, Plasma, Viridis, Cividis
# paleta = Cividis[11]

sqare = [[0,0],[l,0], [l,h], [0, h]]
listPolygons = []

vertex = np.array([[0,0],[l,0], [l,h], [0, h]])
polygon = plt.Polygon(vertex, color = paleta[0], alpha = alpha)
listPolygons.append(polygon)



def frac1(m = 0, sqare = [[0,0],[l,0], [l,h], [0, h]]):

    sqare1 = list(map(f2,sqare))
    sqare2 = list(map(f3,sqare))


    # Dimensiones de la imagen
    for v in range(4):
        if sqare1[v][0]<MinH[0]:
            MinH[0]=sqare1[v][0]
        if sqare1[v][0]>MaxH[0]:
            MaxH[0]=sqare1[v][0]
        if sqare2[v][0]<MinH[0]:
            MinH[0]=sqare2[v][0]
        if sqare2[v][0]>MaxH[0]:
            MaxH[0]=sqare2[v][0]
        
        if sqare1[v][1]<MinV[0]:
            MinV[0]=sqare1[v][1]
        if sqare1[v][1]>MaxV[0]:
            MaxV[0]=sqare1[v][1]
        if sqare2[v][1]<MinV[0]:
            MinV[0]=sqare2[v][1]
        if sqare2[v][1]>MaxV[0]:
            MaxV[0]=sqare2[v][1]
        
    
    #Cuando se ocupa bokeh
    #color = paleta[m%11]
    
    #Paletas en seaborn
    color = paleta[m]
    
    #Para los colores tipo arbol

    """
    if m >5:
        vertex = np.array(sqare1)
        polygon = plt.Polygon(vertex, edgecolor = "green", facecolor = "peru", alpha = alpha)
        listPolygons.append(polygon)
        vertex = np.array(sqare2)
        polygon = plt.Polygon(vertex, edgecolor = "green", facecolor = "peru", alpha = alpha)
        listPolygons.append(polygon)
    else:
        vertex = np.array(sqare1)
        polygon = plt.Polygon(vertex, color = "peru", alpha = alpha)
        listPolygons.append(polygon)
        vertex = np.array(sqare2)
        polygon = plt.Polygon(vertex, color = "peru", alpha = alpha)
        listPolygons.append(polygon)
    """
    
    
    vertex = np.array(sqare1)
    polygon = plt.Polygon(vertex, color = color, alpha = alpha)
    listPolygons.append(polygon)
    vertex = np.array(sqare2)
    polygon = plt.Polygon(vertex, color = color, alpha = alpha)
    listPolygons.append(polygon)
    


    if m<n:
        frac1(m+1, sqare1)
        frac1(m+1, sqare2)
          

fig, ax = plt.subplots(1, 1, figsize=(20,20))
frac1(m = 0, sqare=sqare)
for polygon in listPolygons:
    ax.add_artist(polygon)
    
ax.set_xlim([MinH[0],MaxH[0]])
ax.set_ylim([MinV[0],MaxV[0]])
plt.title(""+str(n)+" recursiones")
ax.set_axis_off()

plt.show()