# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 21:24:32 2017

Script para os dados do TerraClass 


@author: MONGE
"""

from osgeo import gdal,ogr
import numpy as np
#import matplotlib.pyplot as plt



''' Abrindo arquivo SHP do limite do ACRE '''

acre_lm = ogr.Open(r"D:\TESTE\Shp\Acre_LM.shp")
acre_ly = acre_lm.GetLayer()

# Descobrindo os limites do BBox
[xmin,xmax,ymax,ymin] = acre_ly.GetExtent()
print("Xmax:{0:0.4f} \tXmin:{1:0.4f} \nYmax:{2:0.4f} \tYmin:{3:0.4f}".format(xmax,xmin,ymax,ymin))



#''' Descobrindo os Limites dos arquivos Raster '''
nomearquivo = r"D:\TESTE\TerraClass\AC_2004_RASTER.tif"

#Importanto os dados
raster = gdal.Open(nomearquivo)

# Encontrando os valores de BBox e resolução
[xinic,resx,rotax,yinic,rotay,resy] = raster.GetGeoTransform()
xfin = raster.RasterXSize
yfin = raster.RasterYSize
print("Xinic:{0:0.4f} \tResX:{1:0.6f} \nYinic:{2:0.4f} \tResY:{3:0.6f}".format(xinic,resx,yinic,resy))
print("{0} Linhas e {1} Colunas".format(xfin,yfin))


''' Obtendo parametros para gerar a Grade Celular '''
tgc = 200 # tamanho da grade celular retangular
dx = (resx*tgc) # grade de aproximadamente 12 km, por isso 400 pixel
dy = abs(resy*tgc)
nx = int(abs((xmax-xmin)/dx))+1 # obtendo a quantidade de celulas a ser gerada
ny = int(abs((ymax-ymin)/dy))+1
print("Grade celular de {0} por {1}".format(ny,nx))

raster = None # Fecha o arquivo raster aberto

# Loop para todos os outros arquivos da pasta
import os

arq = os.listdir (r"D:\TESTE\TerraClass")
tif = [a for a in arq if a.endswith(".tif")] #obtem apenas os arquivos .tif


# Alocação de memoria 
np_floresta = np.zeros(((ny*nx),len(tif)), dtype=float)
np_floresta.fill(np.nan)

# Para cada ano o ID da Floresta muda, como os arquivos estão 
# em ordem cronologica gera-se uma lista com os ID sequenciados
florestaID = [4,11,10,12,5]

for i in range(len(tif)):
    nomearquivo = (r"D:\TESTE\TerraClass\{0}".format(tif[i]))
    raster = gdal.Open(nomearquivo)

    ''' Cortando Arquivos do MapBiomas '''
    cobertura = raster.ReadAsArray() #lê o arquivo como um array
    floresta = np.where(cobertura==florestaID[i],1,0 )
#    vegsec = np.where(cobertura == 12, 1,0)

    raster = None # Fechar o arquivo raster aberto
    k=0
    rmax = np.max(range(0,ny,1))
    cmax = np.max(range(0,nx,1)) 
    # Loop de calculo de porcentagem por grid
    for r in range(0,rmax+1,1): # Numero de colunas obtidos da nx da grade
        for c in range(0,cmax+1,1):# Numero de linhas obtidos da ny da grade
            if r != rmax  and c != cmax :
                kri = tgc*r
                krf = (tgc*(r+1))-1
                kci = tgc*c
                kcf = (tgc*(c+1))-1
                a = np.nansum(floresta[kri:krf,kci:kcf])
                b = cobertura[kri:krf,kci:kcf]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[k,i]=np.nan
                else:
                    np_floresta[k,i] = round(float(a)/float(b2),6)
                print("Pixel [{0},{1}] \n Celula [{3}:{4}, {5}:{6}] = \tvalor {2}".format(r,c,np_floresta[k,i],kri,krf,kci,kcf))
            
            elif r == rmax and c !=cmax:
                kri = tgc*rmax
                krf = yfin
                kci = (tgc*c)
                kcf = (tgc*(c+1))-1
                a = np.nansum(floresta[kri:krf,kci:kcf])
                b = cobertura[kri:krf,kci:kcf]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[k,i]=np.nan
                else:
                    np_floresta[k,i] = round(float(a)/float(b2),6)
                print("Pixel [{0},{1}] \n Celula [{3}:{4}, {5}:{6}] = \tvalor {2}".format(r,c,np_floresta[k,i],kri,krf,kci,kcf))   
            
            elif r!=rmax and c == cmax:
                kri = (tgc*r)
                krf = (tgc*(r+1))-1
                kci = tgc*cmax
                kcf = xfin 
                a = np.nansum(floresta[kri:krf,kci:kcf])
                b = cobertura[kri:krf,kci:kcf]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                print("Pixel [{0},{1}] \n Celula [{3}:{4}, {5}:{6}] = \tvalor {2}".format(r,c,np_floresta[k,i],kri,krf,kci,kcf))
                
            elif r == rmax and c == cmax:
                [kri,krf,kci,kcf] = (tgc*rmax,yfin,tgc*cmax,xfin)
                a = np.nansum(floresta[kri:krf,kci:krf])
                b = cobertura[kri:krf,kci:krf]
                b1 = np.where(b==255,0,b)
                b2 = np.count_nonzero(b1)
                if b2 ==0:
                    np_floresta[k,i]=np.nan
                else:
                    np_floresta[k,i] = round(float(a)/float(b2),6)
                print("Pixel [{0},{1}] \n Celula [{3}:{4}, {5}:{6}] = \tvalor {2}".format(r,c,np_floresta[k,i],kri,krf,kci,kcf))     
            k+=1    
            
        
    print(tif[i])

cabeca = ("2004;2008;2010;2012;2014")
np.savetxt(r"D:\TESTE\np_floresta.csv",np_floresta,delimiter=";",header=cabeca)


## Calculando as regressões para cada celula

from scipy.stats import linregress


x = (2004,2008,2010,2012,2014)
#y = list(np_floresta[5869])

#m, b, R, p, SEm = linregress(x, y)
# m -declive; b: ordenada na origem; R: coeficiente de correlação (de Pearson)
# p: p-value do teste F em que H0: y = const, independente de x
# SEm: erro padrão do declive

regressao = np.zeros((len(np_floresta),3))

for i in range(len(np_floresta)):
    y = list(np_floresta[i,])
    m, b, R, p, SEm = linregress(x, y)
    regressao[i,0] = m
    regressao[i,1] = R
    regressao[i,2] = p

cabeca = ("2004;2008;2010;2012;2014;decliv;r2;p-val")
np.savetxt("floresta_regressao.csv",np.concatenate((np_floresta,regressao),1),header=cabeca,delimiter=";")

''' Criando o Shapefile da Grade

https://gis.stackexchange.com/questions/54119/creating-square-grid-polygon-shapefile-with-python

'''
from numpy import genfromtxt

tudo = np.genfromtxt('floresta_regressao.csv', delimiter=';')

import shapefile as shp
#import math


w = shp.Writer(shp.POLYGON)
#w.autoBalance = 1
w.field("GRADE",'C')
w.field("F2004",'F',decimal=30)
w.field("F2008",'F',decimal=30)
w.field("F2010",'F',decimal=30)
w.field("F2012",'F',decimal=30)
w.field("F2014",'F',decimal=30)
w.field("decliv",'N',decimal=3)
w.field("r2",'N',decimal=30)
w.field("pval",'N',decimal=30)

id=0
k=0

for i in range(ny):
    for j in range(nx):
        vertices = []
        parts = []
        vertices.append([min(xmin+dx*j,xmax),min(ymax-dy*i,ymin)])
        vertices.append([min(xmin+dx*(j+1),xmax),min(ymax-dy*i,ymin)])
        vertices.append([min(xmin+dx*(j+1),xmax),min(ymax-dy*(i+1),ymin)])
        vertices.append([min(xmin+dx*j,xmax),min(ymax-dy*(i+1),ymin)])
        parts.append(vertices)
        w.poly(parts)
        w.record(GRADE=("R{0}C{1}".format(i,j)),F2004 = np.round(np_floresta[k,0],6), F2008 = np.round(np_floresta[k,1],6), F2010 = np.round(np_floresta[k,2],6), F2012 = np.round(np_floresta[k,3],6), F2014 = np.round(np_floresta[k,4],6), decliv = np.round(tudo[k,5],6), r2 = np.round(tudo[k,6],6), pval = np.round(tudo[k,7],6))
        id+=1
        k+=1
        print("Grade-Celular {0} criada".format(k))

w.save("teste")



