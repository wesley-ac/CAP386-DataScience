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

# Encontrando os valores de BBox e resolução
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



''' Cortando Arquivos do MapBiomas '''

cobertura = raster.ReadAsArray() #lê o arquivo como um array

floresta = np.where(cobertura==4,1,0 )
#vegsec = np.where(cobertura == 12, 1,0)

raster = None # Fechar o arquivo raster aberto

# Alocação de memoria 
np_floresta = np.zeros((ny+1,nx+1), dtype=float)
np_floresta.fill(np.nan)


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
                np_floresta[r,c]=np.nan
            else:
                np_floresta[r,c] = float(a)/float(b2)
            
        elif r == 0 and c != 0:
            kci = (tgc*c)
            kcf = (tgc*(c+1))-1
            a = np.nansum(floresta[0:tgc-1,kci:kcf])
            b = cobertura[0:tgc-1,kci:kcf]
            b1 = np.where(b==255,0,b)
            b2 = np.count_nonzero(b1)
            if b2 ==0:
                np_floresta[r,c]=np.nan
            else:
                np_floresta[r,c] = float(a)/float(b2)
            
        elif r != 0 and c == 0:
            kri = (tgc*r)
            krf = (tgc*(r+1))-1
            a = np.nansum(floresta[kri:krf,0:tgc-1])
            b = cobertura[kri:krf,0:tgc-1]
            b1 = np.where(b==255,0,b)
            b2 = np.count_nonzero(b1)
            if b2 ==0:
                np_floresta[r,c]=np.nan
            else:
                np_floresta[r,c] = float(a)/float(b2)
            
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
                np_floresta[r,c]=np.nan
            else:
                np_floresta[r,c] = float(a)/float(b2)
    
        print("Pixel [{0},{1}] \n Celula [{3}:{4}, {5}:{6}] = \tvalor {2}".format(r,c,np_floresta[r,c],kri,krf,kci,kcf))










