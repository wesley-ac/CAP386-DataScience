Lista de Exercício 03 - 07/07/2017
================

-   [Exercício 01](#Exercicio-01)
-   [Exercício 02](#Exercicio-02)
-   [Exercício 03](#Exercicio-03)
-   [Exercício 04](#Exercicio-04)

Exercício 01
------------

### The “hotdog” variable for the “Hot Dogs in Baltimore” example can be better defined.

#### R.)Existem duas possibilidades, a primeira seria incluir todas as possíveis combinações de maiuscula e minuscula de Hot Dog que existem, e a outra seria utilizar o 'ignore.case = TRUE'

Abrindo o dado

``` r
bVendors <- read.csv(file="./TempData/BFood.csv", header=TRUE, sep=",", stringsAsFactors=FALSE)
```

Caso 1

``` r
grepl("Hot dog|Hot Dog| Hot dogs| Hot Dogs",bVendors$ItemsSold)
```

    ##  [1] FALSE  TRUE  TRUE  TRUE FALSE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE
    ## [12] FALSE  TRUE  TRUE  TRUE  TRUE FALSE  TRUE  TRUE  TRUE FALSE FALSE
    ## [23] FALSE FALSE FALSE FALSE FALSE  TRUE FALSE FALSE FALSE  TRUE  TRUE
    ## [34]  TRUE FALSE  TRUE  TRUE  TRUE  TRUE FALSE FALSE FALSE  TRUE FALSE
    ## [45] FALSE FALSE  TRUE  TRUE FALSE FALSE  TRUE  TRUE FALSE FALSE FALSE
    ## [56]  TRUE FALSE FALSE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE
    ## [67] FALSE  TRUE FALSE  TRUE FALSE FALSE  TRUE FALSE  TRUE  TRUE  TRUE

``` r
grepl("Hot dog|Hot Dogs",bVendors$ItemsSold,ignore.case = TRUE)
```

    ##  [1] FALSE  TRUE  TRUE  TRUE FALSE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE
    ## [12] FALSE  TRUE  TRUE  TRUE  TRUE FALSE  TRUE  TRUE  TRUE  TRUE  TRUE
    ## [23]  TRUE FALSE FALSE  TRUE  TRUE  TRUE  TRUE FALSE FALSE  TRUE  TRUE
    ## [34]  TRUE FALSE  TRUE  TRUE  TRUE  TRUE FALSE  TRUE  TRUE  TRUE FALSE
    ## [45] FALSE  TRUE  TRUE  TRUE FALSE  TRUE  TRUE  TRUE FALSE  TRUE FALSE
    ## [56]  TRUE FALSE FALSE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE
    ## [67] FALSE  TRUE  TRUE  TRUE FALSE  TRUE  TRUE FALSE  TRUE  TRUE  TRUE

Exercício 02
------------

### Create a “pizza” variable then

#### R.)

``` r
grepl("Pizza",bVendors$ItemsSold,ignore.case = TRUE)
```

    ##  [1]  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [12] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [23] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [34] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [45] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [56] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
    ## [67] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE

Exercício 03
------------

### Get the name of the town for the “Hot Dogs in Baltimore”.

#### R.)

``` r
bVendors$TownZ = do.call(rbind,strsplit(bVendors$Location.1,"\n"))[,1]
bVendors$Town = strtrim(bVendors$Town,nchar(bVendors$Town)-6)
bVendors$TownZ = NULL
bVendors$Town[grep("Hot Dog|Hot Dogs",bVendors$ItemsSold,ignore.case = TRUE)]
```

    ##  [1] "Owings Mill"  "Owings Mill"  "Owings Mill"  "Baltimore"   
    ##  [5] "Baltimore"    "Baltimore"    "Baltimore"    "Baltimore"   
    ##  [9] "Baltimore"    "Randallstown" "Baltimore"    "Baltimore"   
    ## [13] "Baltimore"    "Baltimore"    "Baltimore"    "Baltimore"   
    ## [17] "Baltimore"    "Baltimore"    "Baltimore"    "Laurel"      
    ## [21] "Owings Mill"  "Baltimore"    "Baltimore"    "Middle River"
    ## [25] "Baltimore"    "Baltimore"    "Baltimore"    "Reisterstown"
    ## [29] "Reisterstown" "Baltimore"    "Baltimore"    "Baltimore"   
    ## [33] "Baltimore"    "Baltimore"    "Baltimore"    "Windsor Mill"
    ## [37] "Baltimore"    "Baltimore"    "Pikesville"   "Baltimore"   
    ## [41] "Edgewood"     "Baltimore"    "Baltimore"    "Baltimore"   
    ## [45] "Baltimore"    "Baltimore"    "Baltimore"    "Baltimore"   
    ## [49] "Pasadena"     "Baltimore"    "Baltimore"    "Laurel"      
    ## [53] "Baltimore"    "Baltimore"    "Baltimore"    "Baltimore"   
    ## [57] "Pikesville"

Exercício 04
------------

### Complete the Codebook for the “Hot Dogs in Baltimore” example.

Passo 1 - Importando os dados de entrada

``` r
#Armazenando a URL em uma variavel 
site = "https://data.baltimorecity.gov/api/views/bqw3-z52q/rows.csv?accessType=DOWNLOAD"

#Baixa o arquivo e salva na pasta "TempData" com o nome Bfood.csv
#Realiza um teste para ver se já existe um arquivo 
if (file.exists("./TempData/BFood.csv")) 
  {
  tam = file.info("./TempData/BFood.csv")$size # armazena o tamnho do arquivo
  cdata = file.info("./TempData/BFood.csv")$ctime #armazena a data de criação
  paste("Arquivo já existe. ",tam,"bytes. Criado em:",cdata)
  } else
  {
    download.file(site,destfile = "./TempData/BFood.csv",method="curl")
    "Arquivo baixado com sucesso!"
  }
```

    ## [1] "Arquivo já existe.  15661 bytes. Criado em: 2017-07-13 11:10:48"

``` r
bVendors <- read.csv(file="./TempData/BFood.csv", header=TRUE, sep=",", stringsAsFactors=FALSE)

str(bVendors) # Mostra um pedaço do arquivo importado
```

    ## 'data.frame':    77 obs. of  8 variables:
    ##  $ Id        : int  0 0 0 0 0 0 0 0 0 0 ...
    ##  $ LicenseNum: chr  "DF000166" "DF000075" "DF000133" "DF000136" ...
    ##  $ VendorName: chr  "Abdul-Ghani, Christina, \"The Bullpen Bar\"" "Ali, Fathi" "Ali, Fathi" "Ali, Fathi" ...
    ##  $ VendorAddr: chr  "508 Washington Blvd, confined within 10 x 10 space" "SEC Calvert & Madison on Calvert" "NEC Baltimore & Pine Sts" "NEC Light & Redwood Sts" ...
    ##  $ ItemsSold : chr  "Grilled food, pizza slices, gyro sandwiches" "Hot Dogs, Sausage, Snacks, Gum, Candies, Drinks" "Hot dogs, Sausage, drinks, snacks, gum, & candy" "Hot dogs, sausages, chips, snacks, drinks, gum" ...
    ##  $ Cart_Descr: chr  "Two add'l tables to be added to current 6' table in U shape, with grill & warming pans, Tent" "Pushcart" "Pushcart" "Pushcart" ...
    ##  $ St        : chr  "MD" "MD" "MD" "MD" ...
    ##  $ Location.1: chr  "Towson 21204\n(39.28540000000, -76.62260000000)" "Owings Mill 21117\n(39.29860000000, -76.61280000000)" "Owings Mill 21117\n(39.28920000000, -76.62670000000)" "Owings Mill 21117\n(39.28870000000, -76.61360000000)" ...

Passo 2 - Linpando Dados Vazios, desnecessários e Renomeando Colunas

``` r
#Excluindo os dados de ID e ST
bVendors$Id = NULL
bVendors$St = NULL

#Renomeando a coluna Location1
names(bVendors)[names(bVendors) == "Location.1"] <- "location"

str(bVendors)
```

    ## 'data.frame':    77 obs. of  6 variables:
    ##  $ LicenseNum: chr  "DF000166" "DF000075" "DF000133" "DF000136" ...
    ##  $ VendorName: chr  "Abdul-Ghani, Christina, \"The Bullpen Bar\"" "Ali, Fathi" "Ali, Fathi" "Ali, Fathi" ...
    ##  $ VendorAddr: chr  "508 Washington Blvd, confined within 10 x 10 space" "SEC Calvert & Madison on Calvert" "NEC Baltimore & Pine Sts" "NEC Light & Redwood Sts" ...
    ##  $ ItemsSold : chr  "Grilled food, pizza slices, gyro sandwiches" "Hot Dogs, Sausage, Snacks, Gum, Candies, Drinks" "Hot dogs, Sausage, drinks, snacks, gum, & candy" "Hot dogs, sausages, chips, snacks, drinks, gum" ...
    ##  $ Cart_Descr: chr  "Two add'l tables to be added to current 6' table in U shape, with grill & warming pans, Tent" "Pushcart" "Pushcart" "Pushcart" ...
    ##  $ location  : chr  "Towson 21204\n(39.28540000000, -76.62260000000)" "Owings Mill 21117\n(39.29860000000, -76.61280000000)" "Owings Mill 21117\n(39.28920000000, -76.62670000000)" "Owings Mill 21117\n(39.28870000000, -76.61360000000)" ...

Passo 3 - Organizando os dados de Localização

``` r
##Dividindo a coluna de Localização em 4 partes, Town, ZipCode, Lat e Long
# A primeira divisão é quebrar a coluna Location pelo separador '\n' e guardar a primeira parte
bVendors$TownZ = do.call(rbind,strsplit(bVendors$location,"\n"))[,1]

#Retirar da string resultante o nome da Cidade (neste caso foi eliminado os 5 ultimos caracteres referente ao ZIP code)
bVendors$Town = strtrim(bVendors$TownZ,nchar(bVendors$Town)-6)

cat("\nTowns: ", head(bVendors$Town))
```

    ## 
    ## Towns:  Towson Owings Mill Owings Mill Owings Mill Baltimore Baltimore

``` r
# Retirar da primeira parta da string location o ZIPcode (os últimos 5 caracteres)
bVendors$ZIP = substring(bVendors$TownZ,nchar(bVendors$TownZ)-5)

cat("\nZipCode: ", head(bVendors$ZIP))
```

    ## 
    ## ZipCode:   21204  21117  21117  21117  21239  21244

``` r
# Os dados de LAT LONG estão dentro de '()'. Assim foi necessário retirar esses caracteres da segunda parte do string
bVendors$LatLong = do.call(rbind,strsplit(bVendors$location,"\n"))[,2]
bVendors$LatLong = gsub("\\(|)","",bVendors$LatLong)

# Dividiu a coluna de LatLong pelo separador ',' obtendo os resultados de LAT e LONG em colunas individuaizadas
bVendors$Lat = as.numeric(do.call(rbind,strsplit(bVendors$LatLong,","))[,1])
bVendors$Long = as.numeric(do.call(rbind,strsplit(bVendors$LatLong,","))[,2])

cat("\nLatitude: ", head(bVendors$Lat))
```

    ## 
    ## Latitude:  39.2854 39.2986 39.2892 39.2887 39.2792 39.3025

``` r
cat("\nLongitude: ",head(bVendors$Long))
```

    ## 
    ## Longitude:  -76.6226 -76.6128 -76.6267 -76.6136 -76.622 -76.6161

``` r
#Eliminando colunas secundárias
bVendors$location = NULL
bVendors$TownZ = NULL
bVendors$LatLong = NULL
```
