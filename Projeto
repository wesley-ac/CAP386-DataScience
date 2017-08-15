'''
Created on 10 de ago de 2017

@author: Wesley
'''
from osgeo import gdal,ogr
import numpy as np
import matplotlib.pyplot as plt



''' Abrindo arquivo SHP do limite do ACRE '''

acre_lm = ogr.Open("D:/acre_lm.shp")
acre_ly = acre_lm.GetLayer()

# Descobrindo os limites do BBox
[xmin,xmax,ymax,ymin] = acre_ly.GetExtent()
print("Xmax:{0:0.4f} \tXmin:{1:0.4f} \nYmax:{2:0.4f} \tYmin:{3:0.4f}".format(xmax,xmin,ymax,ymin))



#''' Descobrindo os Limites dos arquivos Raster '''
nomearquivo = "D:/AMAZONIA_2000.tif"

#Importanto os dados
raster = gdal.Open(nomearquivo)

# Encontrando os valores de BBox e resolução
[xinic,resx,rotax,yinic,rotay,resy] = raster.GetGeoTransform()
print("Xinic:{0:0.4f} \tResX:{1:0.6f} \nYinic:{2:0.4f} \tResY:{3:0.6f}".format(xinic,resx,yinic,resy))


''' Obtendo parametros para gerar a Grade Celular '''
tgc = 400 # tamanho da grade celular retangular
dx = (resx*tgc) # grade de aproximadamente 12 km, por isso 400 pixel
dy = abs(resy*tgc)
nx = int(abs((xmax-xmin)/dx)) # obtendo a quantidade de celulas a ser gerada
ny = int(abs((ymax-ymin)/dy))


''' Delimitando o BBOx para corte '''
ncol = int((xmin-xinic) / resx) #Numero da linha onde inicia
nrow = int((ymin-yinic) / resy) #Numero da coluna onde inicia
qtcol = (nx+1)*tgc #Quantidade de pixel em colunas que irá buscar, utilizando o numero de celulas criadas
qtrow = (ny+1)*tgc #Quantidade de pixel em linha que irá buscar, utilizando o numero de celulas criadas

print("Retangulo envolvente inicia na linha {0} e coluna {1}, com offset de {2} em X e {3} em Y".format(nrow,ncol,qtcol,qtrow))



''' Cortando Arquivos do MapBiomas '''

mapbioma = raster.ReadAsArray(xoff=nrow,yoff=ncol,xsize=qtcol,ysize=qtrow) #lê o arquivo como um array

floresta = np.where(mapbioma == ((mapbioma == 1) | (mapbioma==2)| (mapbioma==3)| (mapbioma==4)| (mapbioma==5)| (mapbioma==6)| (mapbioma==7)),1,0 )
#vegsec = np.where(mapbioma == 8, 1,0)
#agri = np.where(mapbioma == 14|15|16|17|18|19|20|28|21, 1,0)

# Alocação de memoria 
np_floresta = np.zeros((ny+1,nx+1), dtype=float)
np_floresta.fill(np.nan)


# Loop de calculo de porcentagem por grid
for r in range(0,ny+1,1): # Numero de colunas obtidos da nx da grade
    for c in range(0,nx+1,1): # Numero de linhas obtidos da ny da grade
        if r == 0 and c == 0:
            [kri,krf,kci,kcf] = (0,399,0,399)
            np_floresta[r,c] = floresta[0:399,0:399].sum()/(400*400)
        elif r == 0 and c != 0:
            kci = (400*c)
            kcf = (400*(c+1))-1
            np_floresta[r,c] = floresta[0:399,kci:kcf].sum()/(400*400)
        elif r != 0 and c == 0:
            kri = (400*r)
            krf = (400*(r+1))-1
            np_floresta[r,c] = floresta[kri:krf,0:399,].sum()/(400*400)
        elif r != 0 and c != 0:
            kci = (400*c)
            kcf = (400*(c+1))-1
            kri = (400*r)
            krf = (400*(r+1))-1
            np_floresta[r,c] = floresta[kri:krf,kci:kcf].sum()/(400*400)
    
        print("Pixel [{0},{1}] \n Celula [{3}:{4}, {5}:{6}] = \tvalor {2}".format(r,c,np_floresta[r,c],kri,krf,kci,kcf))


'''
#for numero in range(0,17,1):
    nomearquivo = str("D:/AMAZONIA_20{0:02d}_grd_focos.bin".format(numero))
    print(nomearquivo)
    raster = gdal.Open(nomearquivo)
    mp_cobertura = raster.ReadAsArray(xoff, yoff, xsize, ysize, buf_obj, buf_xsize, buf_ysize, buf_type, resample_alg, callback, callback_data)

