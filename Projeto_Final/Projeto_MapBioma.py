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

acre_lm = ogr.Open(r"D:\TESTE\Shp\Acre_LM.shp")
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
    
   
for i in range(len(tif)):
    nomearquivo = ("D:/TESTE/MapBioma/{0}".format(tif[i]))
    raster = gdal.Open(nomearquivo)
    k=0
    for r in range(0,rmax+1,1): # Numero de colunas obtidos da nx da grade
        for c in range(0,cmax+1,1):# Numero de linhas obtidos da ny da grade
            pxr = nrow+((r+1)*tgc) 
            pxc = ncol+((c+1)*tgc)
            cobertura = raster.ReadAsArray(xoff=pxc,yoff=pxr,xsize=tgc,ysize=tgc).astype(np.float)
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
np.savetxt(r"D:\Teste\np_vegsec_MpBioma.csv",np_vegsec,delimiter=";")
np.savetxt(r"D:\Teste\np_agric_MpBioma.csv",np_agric,delimiter=";")


## Calculando as regressões para cada celula

from scipy.stats import linregress
from numpy import genfromtxt

np_floresta = np.genfromtxt("np_floresta_MpBioma.csv",delimiter=";")
np_vegsec = np.genfromtxt("np_vegsec_MpBioma.csv",delimiter=";")
np_agric = np.genfromtxt("np_agric_MpBioma.csv",delimiter=";")

x = (2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016)
y = list(np_floresta[5869])

m, b, R, p, SEm = linregress(x, y)
# m -declive; b: ordenada na origem; R: coeficiente de correlação (de Pearson)
# p: p-value do teste F em que H0: y = const, independente de x
# SEm: erro padrão do declive

reg_flor = np.zeros((len(np_floresta),3))
reg_vegsec = np.zeros((len(np_floresta),3))
reg_agric = np.zeros((len(np_floresta),3))
dec_flor=[]
sig_flor=[]
dec_vegsec=[]
sig_vegsec=[]
dec_agric = []
sig_agric=[]

for i in range(len(np_floresta)):
    yf = list(np_floresta[i,])
    yv = list(np_vegsec[i,])
    ya = list(np_agric[i,])
    
    # Regressao para floresta
    m, b, R, p, SEm = linregress(x, yf)
    reg_flor[i,0] = m
    if m < 0 :
        dec_flor.append('N')
    elif m == 0 : 
        dec_flor.append('Z')
    elif m > 0:
        dec_flor.append('P')
    else:
        dec_flor.append('')
    reg_flor[i,1] = R
    reg_flor[i,2] = p
    if p<0.05:
       sig_flor.append('S')
    else:
       sig_flor.append('N')
       
    #regressão para vegetação secundaria
    m, b, R, p, SEm = linregress(x, yv)
    reg_vegsec[i,0] = m
    if m < 0 :
        dec_vegsec.append('N')
    elif m == 0 : 
        dec_vegsec.append('Z')
    elif m > 0:
        dec_vegsec.append('P')
    else:
        dec_vegsec.append('')
    reg_vegsec[i,1] = R
    reg_vegsec[i,2] = p
    if p<0.05:
       sig_vegsec.append('S')
    else:
       sig_vegsec.append('N')
    
     #regressão para agricultura
    m, b, R, p, SEm = linregress(x, ya)
    reg_agric[i,0] = m
    if m < 0 :
        dec_agric.append('N')
    elif m == 0 : 
        dec_agric.append('Z')
    elif m > 0:
        dec_agric.append('P')
    else:
        dec_agric.append('')
    reg_agric[i,1] = R
    reg_agric[i,2] = p
    if p<0.05:
       sig_agric.append('S')
    else:
       sig_agric.append('N')
    
    
    print("Celula: k{0}".format(i))

#cabeca = ("2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016;decliv;r2;pval")
#np.savetxt("floresta_regressao_MpBioma.csv",np.concatenate((np_floresta,regressao),1),header=cabeca,delimiter=";")


# Criando o arquivo shape de Grade com os atributos
import shapefile as shp
#import math


z = shp.Writer(shp.POLYGON)
#w.autoBalance = 1
z.field("GRADE",'C')
z.field("F2000",'F',decimal=30)
z.field("F2001",'F',decimal=30)
z.field("F2002",'F',decimal=30)
z.field("F2003",'F',decimal=30)
z.field("F2004",'F',decimal=30)
z.field("F2005",'F',decimal=30)
z.field("F2006",'F',decimal=30)
z.field("F2007",'F',decimal=30)
z.field("F2008",'F',decimal=30)
z.field("F2009",'F',decimal=30)
z.field("F2010",'F',decimal=30)
z.field("F2011",'F',decimal=30)
z.field("F2012",'F',decimal=30)
z.field("F2013",'F',decimal=30)
z.field("F2014",'F',decimal=30)
z.field("F2015",'F',decimal=30)
z.field("F2016",'F',decimal=30)
z.field("decliv",'N',decimal=30)
z.field("sen_decliv",'C')
z.field("r2",'N',decimal=30)
z.field("pval",'N',decimal=30)
z.field("signigcativo",'C')

id=0
k=0

for i in range(ny):
    for j in range(nx):
        vertices = []
        parts = []
        vertices.append([min(xmin+dx*j,xmax),max(ymin-dy*i,ymax)])
        vertices.append([min(xmin+dx*(j+1),xmax),max(ymin-dy*i,ymax)])
        vertices.append([min(xmin+dx*(j+1),xmax),max(ymin-dy*(i+1),ymax)])
        vertices.append([min(xmin+dx*j,xmax),max(ymin-dy*(i+1),ymax)])
        parts.append(vertices)
        z.poly(parts)
        z.record(GRADE=("R{0}C{1}".format(i,j)),
                 F2000 = np.round(np_floresta[k,0],6), 
                 F2001 = np.round(np_floresta[k,1],6), 
                 F2002 = np.round(np_floresta[k,2],6), 
                 F2003 = np.round(np_floresta[k,3],6), 
                 F2004 = np.round(np_floresta[k,4],6), 
                 F2005 = np.round(np_floresta[k,5],6), 
                 F2006 = np.round(np_floresta[k,6],6), 
                 F2007 = np.round(np_floresta[k,7],6), 
                 F2008 = np.round(np_floresta[k,8],6), 
                 F2009 = np.round(np_floresta[k,9],6), 
                 F2010 = np.round(np_floresta[k,10],6), 
                 F2011 = np.round(np_floresta[k,11],6), 
                 F2012 = np.round(np_floresta[k,12],6), 
                 F2013 = np.round(np_floresta[k,13],6), 
                 F2014 = np.round(np_floresta[k,14],6), 
                 F2015 = np.round(np_floresta[k,15],6), 
                 F2016 = np.round(np_floresta[k,16],6), 
                 decliv = np.round(reg_flor[k,0],6), 
                 sen_decliv = dec_flor[k], 
                 r2 = np.round(reg_flor[k,1],6),
                 pval = np.round(reg_flor[k,2],6),
                 signigcativo = sig_flor[k])
#                 )
        id+=1
        k+=1
        print("Grade-Celular {0} criada - R{1}-C{2}".format(k,i,j))

z.save("grade_flor_MpBioma")


z = shp.Writer(shp.POLYGON)
#w.autoBalance = 1
z.field("GRADE",'C')
z.field("F2000",'F',decimal=30)
z.field("F2001",'F',decimal=30)
z.field("F2002",'F',decimal=30)
z.field("F2003",'F',decimal=30)
z.field("F2004",'F',decimal=30)
z.field("F2005",'F',decimal=30)
z.field("F2006",'F',decimal=30)
z.field("F2007",'F',decimal=30)
z.field("F2008",'F',decimal=30)
z.field("F2009",'F',decimal=30)
z.field("F2010",'F',decimal=30)
z.field("F2011",'F',decimal=30)
z.field("F2012",'F',decimal=30)
z.field("F2013",'F',decimal=30)
z.field("F2014",'F',decimal=30)
z.field("F2015",'F',decimal=30)
z.field("F2016",'F',decimal=30)
z.field("decliv",'N',decimal=30)
z.field("sen_decliv",'C')
z.field("r2",'N',decimal=30)
z.field("pval",'N',decimal=30)
z.field("signigcativo",'C')

id=0
k=0

for i in range(ny):
    for j in range(nx):
        vertices = []
        parts = []
        vertices.append([min(xmin+dx*j,xmax),max(ymin-dy*i,ymax)])
        vertices.append([min(xmin+dx*(j+1),xmax),max(ymin-dy*i,ymax)])
        vertices.append([min(xmin+dx*(j+1),xmax),max(ymin-dy*(i+1),ymax)])
        vertices.append([min(xmin+dx*j,xmax),max(ymin-dy*(i+1),ymax)])
        parts.append(vertices)
        z.poly(parts)
        z.record(GRADE=("R{0}C{1}".format(i,j)),
                 F2000 = np.round(np_vegsec[k,0],6), 
                 F2001 = np.round(np_vegsec[k,1],6), 
                 F2002 = np.round(np_vegsec[k,2],6), 
                 F2003 = np.round(np_vegsec[k,3],6), 
                 F2004 = np.round(np_vegsec[k,4],6), 
                 F2005 = np.round(np_vegsec[k,5],6), 
                 F2006 = np.round(np_vegsec[k,6],6), 
                 F2007 = np.round(np_vegsec[k,7],6), 
                 F2008 = np.round(np_vegsec[k,8],6), 
                 F2009 = np.round(np_vegsec[k,9],6), 
                 F2010 = np.round(np_vegsec[k,10],6), 
                 F2011 = np.round(np_vegsec[k,11],6), 
                 F2012 = np.round(np_vegsec[k,12],6), 
                 F2013 = np.round(np_vegsec[k,13],6), 
                 F2014 = np.round(np_vegsec[k,14],6), 
                 F2015 = np.round(np_vegsec[k,15],6), 
                 F2016 = np.round(np_vegsec[k,16],6), 
                 decliv = np.round(reg_vegsec[k,0],6), 
                 sen_decliv = dec_vegsec[k], 
                 r2 = np.round(reg_vegsec[k,1],6),
                 pval = np.round(reg_vegsec[k,2],6),
                 signigcativo = sig_vegsec[k])
#                 )
        id+=1
        k+=1
        print("Grade-Celular {0} criada - R{1}-C{2}".format(k,i,j))

z.save("grade_vegsec_MpBioma")



z = shp.Writer(shp.POLYGON)
#w.autoBalance = 1
z.field("GRADE",'C')
z.field("F2000",'F',decimal=30)
z.field("F2001",'F',decimal=30)
z.field("F2002",'F',decimal=30)
z.field("F2003",'F',decimal=30)
z.field("F2004",'F',decimal=30)
z.field("F2005",'F',decimal=30)
z.field("F2006",'F',decimal=30)
z.field("F2007",'F',decimal=30)
z.field("F2008",'F',decimal=30)
z.field("F2009",'F',decimal=30)
z.field("F2010",'F',decimal=30)
z.field("F2011",'F',decimal=30)
z.field("F2012",'F',decimal=30)
z.field("F2013",'F',decimal=30)
z.field("F2014",'F',decimal=30)
z.field("F2015",'F',decimal=30)
z.field("F2016",'F',decimal=30)
z.field("decliv",'N',decimal=30)
z.field("sen_decliv",'C')
z.field("r2",'N',decimal=30)
z.field("pval",'N',decimal=30)
z.field("signigcativo",'C')

id=0
k=0

for i in range(ny):
    for j in range(nx):
        vertices = []
        parts = []
        vertices.append([min(xmin+dx*j,xmax),max(ymin-dy*i,ymax)])
        vertices.append([min(xmin+dx*(j+1),xmax),max(ymin-dy*i,ymax)])
        vertices.append([min(xmin+dx*(j+1),xmax),max(ymin-dy*(i+1),ymax)])
        vertices.append([min(xmin+dx*j,xmax),max(ymin-dy*(i+1),ymax)])
        parts.append(vertices)
        z.poly(parts)
        z.record(GRADE=("R{0}C{1}".format(i,j)),
                 F2000 = np.round(np_agric[k,0],6), 
                 F2001 = np.round(np_agric[k,1],6), 
                 F2002 = np.round(np_agric[k,2],6), 
                 F2003 = np.round(np_agric[k,3],6), 
                 F2004 = np.round(np_agric[k,4],6), 
                 F2005 = np.round(np_agric[k,5],6), 
                 F2006 = np.round(np_agric[k,6],6), 
                 F2007 = np.round(np_agric[k,7],6), 
                 F2008 = np.round(np_agric[k,8],6), 
                 F2009 = np.round(np_agric[k,9],6), 
                 F2010 = np.round(np_agric[k,10],6), 
                 F2011 = np.round(np_agric[k,11],6), 
                 F2012 = np.round(np_agric[k,12],6), 
                 F2013 = np.round(np_agric[k,13],6), 
                 F2014 = np.round(np_agric[k,14],6), 
                 F2015 = np.round(np_agric[k,15],6), 
                 F2016 = np.round(np_agric[k,16],6), 
                 decliv = np.round(reg_agric[k,0],6), 
                 sen_decliv = dec_agric[k], 
                 r2 = np.round(reg_agric[k,1],6),
                 pval = np.round(reg_agric[k,2],6),
                 signigcativo = sig_agric[k])
#                 )
        id+=1
        k+=1
        print("Grade-Celular {0} criada - R{1}-C{2}".format(k,i,j))

z.save("grade_agric_MpBioma")
