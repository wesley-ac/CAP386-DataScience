# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 21:24:32 2017

Script para os dados do MapBiomas

@author: MONGE
"""

from osgeo import gdal,ogr
import numpy as np
import matplotlib.pyplot as plt



''' Abrindo arquivo SHP do limite do ACRE '''

acre_lm = ogr.Open(r"D:\TESTE\Acre_LM.shp")
acre_ly = acre_lm.GetLayer()

# Descobrindo os limites do BBox
[xmin,xmax,ymax,ymin] = acre_ly.GetExtent()
print("Xmax:{0:0.4f} \tXmin:{1:0.4f} \nYmax:{2:0.4f} \tYmin:{3:0.4f}".format(xmax,xmin,ymax,ymin))



#''' Descobrindo os Limites dos arquivos Raster '''
nomearquivo = r"D:\TESTE\MapBioma\AMAZONIA_2001.tif"

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

raster = None # Fecha o arquivo raster aberto

ncol = int((xmin-xinic) / resx) #Numero da linha onde inicia
nrow = int((ymin-yinic) / resy) #Numero da coluna onde inicia
qtcol = (nx+1)*tgc #Quantidade de pixel em colunas que irá buscar, utilizando o numero de celulas criadas
qtrow = (ny+1)*tgc #Quantidade de pixel em linha que irá buscar, utilizando o numero de celulas criadas

# Loop para todos os outros arquivos da pasta
import os

arq = os.listdir (r"D:\TESTE\MapBioma")
tif = [a for a in arq if a.endswith(".tif")] #obtem apenas os arquivos .tif


# Alocação de memoria 
np_floresta = np.zeros(((ny+1)*(nx+1)+1,len(tif)), dtype=float)
np_floresta.fill(np.nan)

# Para cada ano o ID da Floresta muda, como os arquivos estão 
# em ordem cronologica gera-se uma lista com os ID sequenciados

for i in range(len(tif)):
    nomearquivo = (r"D:\TESTE\MapBioma\{0}".format(tif[i]))
    raster = gdal.Open(nomearquivo)
    mapbioma = raster.ReadAsArray(xoff=nrow,yoff=ncol,xsize=qtcol,ysize=qtrow).astype(np.float)

    ''' Cortando Arquivos do MapBiomas '''
    floresta = np.where(((mapbioma == 3)| (mapbioma==4)| (mapbioma==5)| (mapbioma==6)),1,0 )
    raster = None # Fechar o arquivo raster aberto

    k=0
    # Loop de calculo de porcentagem por grid
    for r in range(0,ny+1,1): # Numero de colunas obtidos da nx da grade
        for c in range(0,nx+1,1):# Numero de linhas obtidos da ny da grade
            k+=1
            if r == 0 and c == 0:
                [kri,krf,kci,kcf] = (0,tgc-1,0,tgc-1)
                a = np.nansum(floresta[0:tgc-1,0:tgc-1])
                b = mapbioma[0:tgc-1,0:tgc-1]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[k,i]=np.nan
                else:
                    np_floresta[k,i] = round(float(a)/float(b2),6)
                
            elif r == 0 and c != 0:
                kci = (tgc*c)
                kcf = (tgc*(c+1))-1
                a = np.nansum(floresta[0:tgc-1,kci:kcf])
                b = mapbioma[0:tgc-1,kci:kcf]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[k,i]=np.nan
                else:
                    np_floresta[k,i] = round(float(a)/float(b2),6)
                
            elif r != 0 and c == 0:
                kri = (tgc*r)
                krf = (tgc*(r+1))-1
                a = np.nansum(floresta[kri:krf,0:tgc-1])
                b = mapbioma[kri:krf,0:tgc-1]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[k,i]=np.nan
                else:
                    np_floresta[k,i] = round(float(a)/float(b2),6)
                
            elif r != 0 and c != 0:
                kci = (tgc*c)
                kcf = (tgc*(c+1))-1
                kri = (tgc*r)
                krf = (tgc*(r+1))-1
                a = np.nansum(floresta[kri:krf,kci:kcf])
                b = mapbioma[kri:krf,kci:kcf]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[k,i]=np.nan
                else:
                    np_floresta[k,i] = round(float(a)/float(b2),6)
        
            #print("Pixel [{0},{1}] \n Celula [{3}:{4}, {5}:{6}] = \tvalor {2}".format(r,c,np_floresta[r,c],kri,krf,kci,kcf))
    floresta = None
    mapbioma = None
    print(tif[i])

np.savetxt("np_floresta.csv",np_floresta,delimiter=";")


## Calculando as regressões para cada celula

#from scipy.stats import linregress


#x = (2004,2008,2010,2012,2014)
#y = list(np_floresta[5869])

#m, b, R, p, SEm = linregress(x, y)
# m -declive; b: ordenada na origem; R: coeficiente de correlação (de Pearson)
# p: p-value do teste F em que H0: y = const, independente de x
# SEm: erro padrão do declive

#regressao = np.zeros((len(np_floresta),3))

#for i in range(len(np_floresta)):
#    y = list(np_floresta[i,])
#    m, b, R, p, SEm = linregress(x, y)
#    regressao[i,0] = m
#    regressao[i,1] = R
#    regressao[i,2] = p

#cabeca = ("2004;2008;2010;2012;2014;decliv;r2;p-val")
#np.savetxt("floresta_regressao.csv",np.concatenate((np_floresta,regressao),1),header=cabeca,delimiter=";")


