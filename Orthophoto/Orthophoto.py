# -*- coding: utf-8 -*-
"""
Created on Thu May  5 11:16:48 2022
@author: Silvia Mourao
"""
# =============================================================================
# #Programa Ortofoto
# =============================================================================

import numpy as np
import math
import matplotlib.pyplot as plt
import imageio
import tifffile as tiff

plt.close('all');

# =============================================================================
# #Definir Parâmetros Orientação Externa
# #Foto 10
# =============================================================================
  
X0=-88862.817  
Y0=-100775.419
Z0=1095.119    
Omega=0.8104*math.pi/180
Phi=0.7361*math.pi/180
Kappa=13.6430*math.pi/180

# =============================================================================
# #Definir Parâmetros Orientação Interna
# #Certificado Camera
# =============================================================================

c=0.12
x0=0
y0=0
px=12*10**(-6)


# =============================================================================
# #Matriz de Rotação
# =============================================================================

r11=(math.cos(Phi))*(math.cos(Kappa))
r12=-(math.cos(Phi))*(math.sin(Kappa))
r13=math.sin(Phi)
r21=(math.cos(Omega))*(math.sin(Kappa))+(math.sin(Omega))*(math.sin(Phi))*(math.cos(Kappa))
r22=(math.cos(Omega))*(math.cos(Kappa))-(math.sin(Omega))*(math.sin(Phi))*(math.sin(Kappa))
r23=-(math.sin(Omega))*(math.cos(Phi))
r31=(math.sin(Omega))*(math.sin(Kappa))-(math.cos(Omega))*(math.sin(Phi))*(math.cos(Kappa))
r32=(math.sin(Omega))*(math.cos(Kappa))+(math.cos(Omega))*(math.sin(Phi))*(math.sin(Kappa))
r33=(math.cos(Omega))*(math.cos(Phi))

R= [[r11,r12,r13],
    [r21,r22,r23],
    [r31,r32,r33]]


# =============================================================================
# #Importar Foto
# =============================================================================

foto10 = tiff.imread('10.tif')

# Parâmetros da foto original
lin=foto10.shape[0]
col=foto10.shape[1]


# =============================================================================
# #Importar Telha LIDAR
# =============================================================================

telha  = np.loadtxt("telha.txt", skiprows=6)

#Dimensões da ortofoto final correspondem ás dimensões da telha
#500 linhas, 500 colunas, 3 bandas de cor

Orto=np.zeros((500,500,3))

#A telha apenas tem coordenadas do canto inferior esquerdo em XYZ
#seguidas apenas de coordenadas Z, em intervalos de 1 metro

#Coordenada na origem da Telha
XLL=-89005.483600000007
YLL=-100982.793600000000

#Ciclo que calcula as coordenadas XY para todas as coordenadas Z da telha

X=np.zeros(telha.shape)
Y=np.zeros(telha.shape)
Z=np.zeros(telha.shape)

for i in range(500):
    for j in range(500):
        Xll=XLL
        Yll=YLL
        X[i][j]=(Xll+j)
        Y[i][j]=(Yll+i)
        Z[i][j]=(telha[i][j])

#A origem das coordenadas da telha está no canto inferior esquerdo
#A origem das coordenadas pixel de uma foto está no canto superior esquerdo
#é necessário "virar" a matriz de coordenadas da telha para que estas se correspondam

X=np.flipud(X)
Y=np.flipud(Y)
Z=np.flipud(Z)

# =============================================================================
# #Aplicação das Eq. Colinearidade para transformação de coordenadas terreno
# para coordenadas foto   
# =============================================================================

x_coli=np.zeros(telha.shape)
y_coli=np.zeros(telha.shape)
for i in range(500):
    for j in range(500):
        Nx=r11*(X[i][j]-X0)+r21*(Y[i][j]-Y0)+r31*(Z[i][j]-Z0)
        Ny=r12*(X[i][j]-X0)+r22*(Y[i][j]-Y0)+r32*(Z[i][j]-Z0)
        D=r13*(X[i][j]-X0)+r23*(Y[i][j]-Y0)+r33*(Z[i][j]-Z0)
        x_coli[i][j]=x0-c*(Nx/D)
        y_coli[i][j]=y0-c*(Ny/D)
        

# =============================================================================
# # Foto Digital está em coordenadas pixel, é necessário converter para
# # coordenadas foto
# =============================================================================

xp=np.zeros(telha.shape)
yp=np.zeros(telha.shape)  
xci=np.zeros(telha.shape)
yci=np.zeros(telha.shape)
foto=foto10.copy()

for i in range(500):
    for j in range(500):
        xci[i][j]=x_coli[i][j]/px
        yci[i][j]=y_coli[i][j]/px
        xp[i][j]=xci[i][j]+col/2
        yp[i][j]=lin/2-yci[i][j]
        
# =============================================================================
# # Após converter coordenadas, estas percorrem um ciclo na foto original para
# encontrar a cor do pixel e coloca-lo na imagem final em RGB       
# =============================================================================
        
        if (yp[i][j]>=lin) or (xp[i][j]>=col):
            yp[i][j]=lin-1
            xp[i][j]=col-1
            foto[int(yp[i][j])][int(xp[i][j])][0]=0
            foto[int(yp[i][j])][int(xp[i][j])][1]=0
            foto[int(yp[i][j])][int(xp[i][j])][2]=0
            
        Orto[i][j][0]=foto[int(yp[i][j])][int(xp[i][j])][0]
        Orto[i][j][1]=foto[int(yp[i][j])][int(xp[i][j])][1]
        Orto[i][j][2]=foto[int(yp[i][j])][int(xp[i][j])][2]


#Ortofoto resultante e telha
I=np.uint8(Orto)

plt.subplot(221);plt.imshow(I);plt.title("Ortofoto");plt.axis("off")        
plt.subplot(222);plt.imshow(I[:,:,1]);plt.title("Ortofoto sem RGB");plt.axis("off")  
plt.subplot(223);plt.imshow(telha, 'gray');plt.title("Telha cinzento");plt.axis("off")  
plt.subplot(224);plt.imshow(telha);plt.title("Telha");plt.axis("off")  

a=imageio.imwrite('Orto.tif',I[:,:,:])

