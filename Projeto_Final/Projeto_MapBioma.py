# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 21:24:32 2017

Script para os dados do MapBiomas

@author: MONGE
"""

from osgeo import gdal,ogr
import numpy as np
#import matplotlib.pyplot as plt



''' Abrindo arquivo SHP do limite do ACRE '''

acre_lm = ogr.Open(r"D:\TESTE\Acre_LM.shp")
acre_ly = acre_lm.GetLayer()

# Descobrindo os limites do BBox
[xmin,xmax,ymax,ymin] = acre_ly.GetExtent()
print("Xmax:{0:0.4f} \tXmin:{1:0.4f} \nYmax:{2:0.4f} \tYmin:{3:0.4f}".format(xmax,xmin,ymax,ymin))

acre_lm=None
acre_ly=None

#''' Descobrindo os Limites dos arquivos Raster '''
nomearquivo = r"D:\TESTE\MapBioma\AMAZONIA_2000.tif"

#Importanto os dados
raster = gdal.Open(nomearquivo)

# Encontrando os valores de BBox e resolução
[xinic,resx,rotax,yinic,rotay,resy] = raster.GetGeoTransform()
print("Xinic:{0:0.4f} \tResX:{1:0.6f} \nYinic:{2:0.4f} \tResY:{3:0.6f}".format(xinic,resx,yinic,resy))
print("{0} Linhas e {1} Colunas".format(raster.RasterXSize,raster.RasterYSize))


''' Obtendo parametros para gerar a Grade Celular '''
tgc = 200 # tamanho da grade celular retangular
dx = (resx*tgc) # grade de aproximadamente 6 km, por isso 200 pixel
dy = abs(resy*tgc)
nx = int(abs((xmax-xmin)/dx))+1 # obtendo a quantidade de celulas a ser gerada
ny = int(abs((ymax-ymin)/dy))+1
print("Grade celular de {0} por {1}".format(ny,nx))

raster = None # Fecha o arquivo raster aberto

ncol = int((xmin-xinic) / resx) #Numero da linha onde inicia
nrow = int((ymin-yinic) / resy) #Numero da coluna onde inicia
qtcol = (nx+1)*tgc #Quantidade de pixel em colunas que irá buscar, utilizando o numero de celulas criadas
qtrow = (ny+1)*tgc #Quantidade de pixel em linha que irá buscar, utilizando o numero de celulas criadas
print("Retangulo envolvente inicia na linha {0} e coluna {1}, com offset de {2} em X e {3} em Y".format(nrow,ncol,qtcol,qtrow))

# Loop para todos os outros arquivos da pasta
import os

arq = os.listdir (r"D:\TESTE\MapBioma")
tif = [a for a in arq if a.endswith(".tif")] #obtem apenas os arquivos .tif


# Alocação de memoria 
np_floresta = np.zeros(((ny*nx)+1,len(tif)), dtype=float)
np_floresta.fill(np.nan)
np_vegsec = np.zeros(((ny*nx)+1,len(tif)), dtype=float)
np_vegsec.fill(np.nan)
np_agric = np.zeros(((ny*nx)+1,len(tif)), dtype=float)
np_agric.fill(np.nan)

rmax = np.max(range(0,ny,1))
cmax = np.max(range(0,nx,1)) 
    
k=0
    
for i in range(len(tif)):
    nomearquivo = (r"D:\TESTE\MapBioma\{0}".format(tif[i]))
    raster = gdal.Open(nomearquivo)
    
    for r in range(0,rmax+1,1): # Numero de colunas obtidos da nx da grade
        for c in range(0,cmax+1,1):# Numero de linhas obtidos da ny da grade
            pxr = nrow+((r+1)*tgc) 
            pxc = ncol+((c+1)*tgc)
            cobertura = raster.ReadAsArray(xoff=pxr,yoff=pxc,xsize=tgc,ysize=tgc).astype(np.float)
            floresta = np.where(((cobertura == 3)| (cobertura==4)| (cobertura==5)| (cobertura==6)),1.,0 )
            vegsec = np.where(((cobertura == 7)| (cobertura==8)),1.,0 )
            agric = np.where(((cobertura == 15)| (cobertura==19)| (cobertura==20)| (cobertura==21)| (cobertura==28)),1.,0 )
            flo = floresta.sum()
            vegs = vegsec.sum()
            ag = agric.sum()
            b = np.count_nonzero(cobertura)
            if b ==0:
                np_floresta[k,i] = np.nan
                np_vegsec[k,i] = np.nan
                np_agric[k,i] = np.nan
            else:
                np_floresta[k,i] = round(float(flo)/float(b),6)
                np_vegsec[k,i] = round(float(vegs)/float(b),6)
                np_agric[k,i] = round(float(ag)/float(b),6)
                print("Pixel [{0},{1}] \n Celula - xinix:{3}, yinic:{4}] = \tvalor {2}".format(r,c,np_floresta[k,i],pxr,pxc))
               
            k+=1    
            
        
    print(tif[i])

np.savetxt(r"D:\Teste\np_floresta_MpBioma.csv",np_floresta,delimiter=";")
np.savetxt(r"D:\Teste\np_vegsec_MpBioma.csv",np_floresta,delimiter=";")
np.savetxt(r"D:\Teste\np_agric_MpBioma.csv",np_floresta,delimiter=";")


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


