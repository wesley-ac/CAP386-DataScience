# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 21:24:32 2017

@author: MONGE
"""

from osgeo import gdal,ogr
import numpy as np
import matplotlib.pyplot as plt



''' Abrindo arquivo SHP do limite do ACRE '''

acre_lm = ogr.Open("./Shp/Acre_LM.shp")
acre_ly = acre_lm.GetLayer()

# Descobrindo os limites do BBox
[xmin,xmax,ymax,ymin] = acre_ly.GetExtent()
print("Xmax:{0:0.4f} \tXmin:{1:0.4f} \nYmax:{2:0.4f} \tYmin:{3:0.4f}".format(xmax,xmin,ymax,ymin))



#''' Descobrindo os Limites dos arquivos Raster '''
nomearquivo = "./TerraClass/AC_2004_RASTER.tif"

#Importanto os dados
raster = gdal.Open(nomearquivo)

# Encontrando os valores de BBox e resoluÃ§Ã£o
[xinic,resx,rotax,yinic,rotay,resy] = raster.GetGeoTransform()
print("Xinic:{0:0.4f} \tResX:{1:0.6f} \nYinic:{2:0.4f} \tResY:{3:0.6f}".format(xinic,resx,yinic,resy))
print("{0} Linhas e {1} Colunas".format(raster.RasterXSize,raster.RasterYSize))


''' Obtendo parametros para gerar a Grade Celular '''
tgc = 200 # tamanho da grade celular retangular
dx = (resx*tgc) # grade de aproximadamente 12 km, por isso 400 pixel
dy = abs(resy*tgc)
nx = int(abs((xmax-xmin)/dx)) # obtendo a quantidade de celulas a ser gerada
ny = int(abs((ymax-ymin)/dy))
print("Grade celular de {0} por {1}".format(ny,nx))

raster = None # Fecha o arquivo raster aberto

# Loop para todos os outros arquivos da pasta
import os

arq = os.listdir ("./TerraClass")
tif = [a for a in arq if a.endswith(".tif")] #obtem apenas os arquivos .tif


# AlocaÃ§Ã£o de memoria 
np_floresta = np.zeros((len(tif),ny+1,nx+1), dtype=float)
np_floresta.fill(np.nan)

for i in range(len(tif)):
    nomearquivo = "./TerraClass/"+tif[i]
    raster = gdal.Open(nomearquivo)

    ''' Cortando Arquivos do MapBiomas '''
    cobertura = raster.ReadAsArray() #lÃª o arquivo como um array
    floresta = np.where(cobertura==4,1,0 )
#    vegsec = np.where(cobertura == 12, 1,0)

    raster = None # Fechar o arquivo raster aberto

    # Loop de calculo de porcentagem por grid
    for r in range(0,ny+1,1): # Numero de colunas obtidos da nx da grade
        for c in range(0,nx+1,1): # Numero de linhas obtidos da ny da grade
            if r == 0 and c == 0:
                [kri,krf,kci,kcf] = (0,tgc-1,0,tgc-1)
                a = np.nansum(floresta[0:tgc-1,0:tgc-1])
                b = cobertura[0:tgc-1,0:tgc-1]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[i,r,c]=np.nan
                else:
                    np_floresta[i,r,c] = float(a)/float(b2)
                
            elif r == 0 and c != 0:
                kci = (tgc*c)
                kcf = (tgc*(c+1))-1
                a = np.nansum(floresta[0:tgc-1,kci:kcf])
                b = cobertura[0:tgc-1,kci:kcf]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[i,r,c]=np.nan
                else:
                    np_floresta[i,r,c] = float(a)/float(b2)
                
            elif r != 0 and c == 0:
                kri = (tgc*r)
                krf = (tgc*(r+1))-1
                a = np.nansum(floresta[kri:krf,0:tgc-1])
                b = cobertura[kri:krf,0:tgc-1]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[i,r,c]=np.nan
                else:
                    np_floresta[i,r,c] = float(a)/float(b2)
                
            elif r != 0 and c != 0:
                kci = (tgc*c)
                kcf = (tgc*(c+1))-1
                kri = (tgc*r)
                krf = (tgc*(r+1))-1
                a = np.nansum(floresta[kri:krf,kci:kcf])
                b = cobertura[kri:krf,kci:kcf]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[i,r,c]=np.nan
                else:
                    np_floresta[i,r,c] = float(a)/float(b2)
        
            #print("Pixel [{0},{1}] \n Celula [{3}:{4}, {5}:{6}] = \tvalor {2}".format(r,c,np_floresta[r,c],kri,krf,kci,kcf))
    print(tif[i])


f, axarr = plt.subplots(len(tif), sharex=True)
for i in range(len(tif)):
    axarr[i].plt.imshow(np_floresta[i])
    axarr[i].set_title(tif[i])

f, (ax1, ax2,ax3,ax4,ax5) = plt.subplots(5, 1, sharex=True)
ax1.imshow(np_floresta[0])
ax1.set_title(tif[0])
ax2.imshow(np_floresta[1])
ax2.set_title(tif[1])
ax3.imshow(np_floresta[2])
ax3.set_title(tif[2])
ax4.imshow(np_floresta[3])
ax4.set_title(tif[3])
ax5.imshow(np_floresta[4])
ax5.set_title(tif[4])
ax5.colorbar()








