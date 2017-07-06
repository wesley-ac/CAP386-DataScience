Exercicio\_02
================

Exercício Semana 2 - 30/06/2017
===============================

### 1) Understanding and Fixing Code

#### 1.1) Fix the part of the code that shows the cold months in Baltimore (Lecture02/04-OperationsWithVectors) so we know which are those months.

##### R:) O Problema encontrado foi que não houve a definição dos **nomes** dos meses para a variavel `tempLo`, uma forma de corrigir é relaizar :

``` r
tempLo <- c(23.5,26.1,33.6,42.0,51.8,60.8,65.8,63.9,56.6,43.7,34.7,27.3)
months <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
names(tempLo) <- months
tempLo
```

    ##  Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec 
    ## 23.5 26.1 33.6 42.0 51.8 60.8 65.8 63.9 56.6 43.7 34.7 27.3

Assim quando se realizar a expressão abaixo o resultado retornará com os nomes dos meses.

``` r
tooCold <- (((5/9) * (tempLo - 32)) < 0)
tooCold
```

    ##   Jan   Feb   Mar   Apr   May   Jun   Jul   Aug   Sep   Oct   Nov   Dec 
    ##  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE

#### 1.2) What would happen if we still had a NA on the vector for the temperatures in SJC (Lecture02/05-Factors)?

``` r
avgTempSJC <- c(22.2,22.4,21.6,19.6,17,16.1,15.6,17.1,18.8,19.4,20.3,21.4)
names(avgTempSJC) <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
avgTempSJC
```

    ##  Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec 
    ## 22.2 22.4 21.6 19.6 17.0 16.1 15.6 17.1 18.8 19.4 20.3 21.4

##### R:) Se houvesse `NA` em `avgTempSJC` o resultado da expressão abaixo seria `FALSE` para os locais com `NA`, como observado a seguir:

``` r
avgTempSJC <- c(22.2,NA,21.6,19.6,17,16.1,NA,17.1,18.8,19.4,20.3,NA)
names(avgTempSJC) <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")

descTempSJC <- vector(length = length(avgTempSJC))
descTempSJC[avgTempSJC>20] <- 'Hot' 
descTempSJC[(avgTempSJC >= 18) & (avgTempSJC <= 20)] <- 'Mild'
descTempSJC[avgTempSJC<18] <- 'Cool' 
descTempSJC
```

    ##  [1] "Hot"   "FALSE" "Hot"   "Mild"  "Cool"  "Cool"  "FALSE" "Cool" 
    ##  [9] "Mild"  "Mild"  "Hot"   "FALSE"

#### 1.3) What happens if we try to run sjcTemps\["Jan":"Jul",c(1,3)\]? Why? (see Lecture02/06-DataFrames).

O Data Frame sjcTemps é representado por:

``` r
maxTempSJC <- c(29.7,30.1,29.5,27.3,25.1,24.3,24.1,26.2,27.2,27.3,28,28.7)
avgTempSJC <- c(22.2,22.4,21.6,19.6,17,16.1,15.6,17.1,18.8,19.4,20.3,21.4)
minTempSJC <- c(16.2,16.5,15.7,13.2,10.1,8.9,8.2,9.9,11.9,13.4,14.2,15.3)
months <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
sjcTemps <- data.frame(Max=maxTempSJC,Avg=avgTempSJC,Min=minTempSJC,row.names = months)
sjcTemps
```

    ##      Max  Avg  Min
    ## Jan 29.7 22.2 16.2
    ## Feb 30.1 22.4 16.5
    ## Mar 29.5 21.6 15.7
    ## Apr 27.3 19.6 13.2
    ## May 25.1 17.0 10.1
    ## Jun 24.3 16.1  8.9
    ## Jul 24.1 15.6  8.2
    ## Aug 26.2 17.1  9.9
    ## Sep 27.2 18.8 11.9
    ## Oct 27.3 19.4 13.4
    ## Nov 28.0 20.3 14.2
    ## Dec 28.7 21.4 15.3

##### R:) Se aplicassemos a expressão `sjcTemps["Jan":"Jul",c(1,3)]` retornaria erro pois o R não interpreta que os caracteres estejam em um intervalo:

``` r
sjcTemps["Jan":"Jul",c(1,3)]
```

Entretanto, se alterar a expressão para `sjcTemps[c("Jan","Jul"),c(1,3)]` irá retornar os valores de Jan e Jul

``` r
sjcTemps[c("Jan","Jul"),c(1,3)]
```

    ##      Max  Min
    ## Jan 29.7 16.2
    ## Jul 24.1  8.2

Porém se o objetivo é retornar os valores entre Jan e Jul, o indicado seria incluir o intervalo das linhas `1:6`

``` r
sjcTemps[c(1:6),c(1,3)]
```

    ##      Max  Min
    ## Jan 29.7 16.2
    ## Feb 30.1 16.5
    ## Mar 29.5 15.7
    ## Apr 27.3 13.2
    ## May 25.1 10.1
    ## Jun 24.3  8.9

#### 1.4) We can change Data Frames with `sjcTemps3["Aug",] <- c(1,2,3)` and `sjcTemps3["Jul",] <- sjcTemps3["Jul",]+c(3,4)` but we cannot change with `sjcTemps3["Jul",] <- c(3,4)`. Why? (see Lecture02/06-DataFrames).

##### R:) A expressão `sjcTemps3["Aug",] <- c(1,2,3)` altera os valores pois a quantidade de valores da tabela é a mesma da tupla a ser inserida; A expressão `sjcTemps3["Jul",] <- sjcTemps3["Jul",]+c(3,4)` passa pela condicionante pois esta dentro de uma operação. Porém quando se realiza a expressão `sjcTemps3["Jul",] <- c(3,4)` o R reporta um erro de tamanho da tupla para a regra da reciclagem.

#### 1.5) Run some examples that show that the recycling rule reuses the smaller (shorter) vector.

##### R:)

``` r
a <- c(0,0,0,0,0,0)
a
```

    ## [1] 0 0 0 0 0 0

Exemplo 1:

``` r
b <- a
b <- a+ c(1)
b
```

    ## [1] 1 1 1 1 1 1

Exemplo 2:

``` r
d <- a
d <- a+c(1,2)
d
```

    ## [1] 1 2 1 2 1 2

Exemplo 3:

``` r
e <- a
e <- a + c(1,2,3)
e
```

    ## [1] 1 2 3 1 2 3

Exemplo 4:

``` r
f <- a 
f <- a+c(1,2,3,4)
```

    ## Warning in a + c(1, 2, 3, 4): comprimento do objeto maior não é múltiplo do
    ## comprimento do objeto menor

``` r
f
```

    ## [1] 1 2 3 4 1 2

#### 1.6) What does stringsAsFactors=FALSE in read.csv() do? Why do we need it? (see Lecture02/06-DataFrames).

##### R) A função `stringsAsFactors=FALSE` transforma as colunas do tipo string em fatores, com isso os meses seriam transformados em fatores e ordenando-os de forma alfabética, prejudicando a apresentação da tabela e outras formas de manipulação.

### 2) The average monthly rainfall in Baltimore is, in inches: 3.47, 3.02, 3.93, 3.00, 3.89, 3.43, 3.85, 3.74, 3.98, 3.16, 3.12, 3.35 (<http://www.rssweather.com/climate/Maryland/Baltimore/>) Write an R program that shows this in millimeters (one inch = 25.4 mm), add names to the vector, and calculates its average, minimum and maximum.

``` r
precipita_inch <- c(3.47, 3.02, 3.93, 3.00, 3.89, 3.43, 3.85, 3.74, 3.98, 3.16, 3.12, 3.35)
meses <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")

precipita_mm <- precipita_inch * 25.4
names(precipita_mm) <- meses
precipita_mm
```

    ##     Jan     Feb     Mar     Apr     May     Jun     Jul     Aug     Sep 
    ##  88.138  76.708  99.822  76.200  98.806  87.122  97.790  94.996 101.092 
    ##     Oct     Nov     Dec 
    ##  80.264  79.248  85.090

``` r
prec_max <- max(precipita_mm)
prec_min <- min(precipita_mm)
prec_avg <- mean(precipita_mm)
cat("\nPrecipitação máxima: ", prec_max)
```

    ## 
    ## Precipitação máxima:  101.092

``` r
cat("\nPrecipitação minima: ", prec_min)
```

    ## 
    ## Precipitação minima:  76.2

``` r
cat ("\nPrecipitação média: ", prec_avg)
```

    ## 
    ## Precipitação média:  88.773
