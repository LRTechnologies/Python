import math
import time
m=4096
minutosSimulados=480 #8horas
tiemposFila1=[]
#FUNCION PARA OBTENER PROMEDIO DE UN ARRAY
def promedio(array):return sum(array)/len(array)
def numAleatorio(multiplicador,const,semilla):
    arrayTemporal=[]#aleatorios enteros
    arrayUniforme=[]#aleatorios entre 0 y 1
    arrayTemporal.append(semilla)
    for x in range(m):
        a = ((multiplicador * arrayTemporal[x]) + const) % m
        arrayTemporal.append(a)
    #CONVERTIRLOS EN UNIFORME ENTRE  0 y 1
    for x in arrayTemporal:        
        arrayUniforme.append(x/m)
    return arrayUniforme

def numero(num):
        numDecimales=2
        cadena=str(num)
        if "." in cadena:
            cadena=cadena[0:cadena.index(".")+(numDecimales+1)]
        return float(cadena)

def mayor(a,b):return numero(max(a,b))
def exponencial(beta,ri):return ((-beta)*math.log(ri))
def uniforme(a,b,ri):return (a+(b-a)*ri)

def iniciarSimulacion(listaValores,nombreArchivo):
    random1=numAleatorio(listaValores[0],listaValores[1],listaValores[2])
    random2=numAleatorio(listaValores[3],listaValores[4],listaValores[5])
    random3=numAleatorio(listaValores[6],listaValores[7],listaValores[8])
    tiemposTotalSistema=[]
    numCliente=0  

    #LLEGADAS ESTACION1
    intervalos=[]#intervalos en los que llegan clientes
    llegadas=[]#acumular intervalos para determinar horas de llegada
    sumaLlegadas=0

    while sumaLlegadas<minutosSimulados:
        llegada_actual=exponencial(3,random1[numCliente])#3 minutos llegadas
        sumaLlegadas+=llegada_actual
        llegadas.append(numero(sumaLlegadas))
        intervalos.append(llegada_actual)
        numCliente+=1
    numCliente=0

    #TIEMPO SERVICIO E1
    servicios1=[]
    sumaServicio1=0
    while sumaServicio1<minutosSimulados:
        serv=numero(exponencial(2,random2[numCliente]))#2 minutos de servicio en la estacion1
        sumaServicio1+=serv
        servicios1.append(serv)
        numCliente+=1
    numCliente=0

    #TIEMPO SERVICIO E2
    servicios2=[]
    sumaServicio2=0
    while sumaServicio2<minutosSimulados:
        serv=numero(uniforme(1,2,random3[numCliente]))#2 minutos de servicio en la estacion1
        sumaServicio2+=serv
        servicios2.append(serv)
        numCliente+=1
    numCliente=0

    #HORAS DE ENTRADA Y SALIDA A ESTACION 1
    entradas1=[]
    salidas1=[]
    index=0
    for x in llegadas:
        if(len(salidas1)==0):
            entradas1.append(llegadas[0])
            salidas1.append(entradas1[0]+servicios1[0])
        else:
            entradas1.append(mayor(llegadas[index],salidas1[index-1]))#OK
            salidas1.append(numero(entradas1[index]+servicios1[index]))
        index+=1

    #HORAS DE ENTRADA Y SALIDA A ESTACION 2
    entradas2=[]
    salidas2=[]
    index=0
    for x in salidas1:
        if(len(salidas2)==0):
            entradas2.append(salidas1[0])
            salidas2.append(entradas2[0]+servicios2[0])
        else:
            entradas2.append(mayor(salidas1[index],salidas2[index-1]))#OK
            salidas2.append(numero(entradas2[index]+servicios2[index]))
        index+=1

    #CALCULAR TIEMPOS TOTALES EN EL SISTEMA PARA CADA CLIENTE
    tiempos=[]
    contador=0
    for x in llegadas:
        tiempos.append(salidas2[contador]-llegadas[contador])
        contador+=1

    #CALCULAR FILA MAYOR
    f=0
    fila1=0
    fila2=0
    for a in llegadas:
        if(entradas1[f]>llegadas[f]):fila1+=1
        if(entradas2[f]>salidas1[f]):fila2+=1
        f+=1

    #IMPRIMIR ARCHIVO
    n=0    
    archivo=open("c:/python/"+nombreArchivo,"w")
    archivo.write("PROMEDIO:,"+str(promedio(tiempos))+",MINUTOS\n")
    archivo.write("FILA E1:,"+str(fila1)+",CLIENTES\n")
    archivo.write("FILA E2:,"+str(fila2)+",CLIENTES\n")
    archivo.write("CLIENTE,LLEGADAS,ENTRADA E1,SERV E1,SALIDA E1,ENTRADA E2,SERV E2,SALIDA E2,TIEMPOTOTAL,TMP FILA1\n")
    for x in llegadas:
        tiemposTotalSistema.append(tiempos[n])
        tiempoFila1=entradas1[n]-llegadas[n];
        tiemposFila1.append(tiempoFila1)
        txt="";
        txt+=(str(n)+",")
        txt+=(str(llegadas[n])+",")
        txt+=(str(entradas1[n])+",")
        txt+=(str(servicios1[n])+",")
        txt+=(str(salidas1[n])+",")
        txt+=(str(entradas2[n])+",")
        txt+=(str(servicios2[n])+",")
        txt+=(str(salidas2[n])+",")
        txt+=(str(tiempos[n])+",")
        txt+=(str(tiempoFila1)+"\n")
        archivo.write(txt)
        n+=1
    archivo.close()
    time.sleep(0.1)
    print(str(promedio(tiemposFila1)))

iniciarSimulacion([3,3,6,7,3,38,9,6,17],"simulacion1.csv")
iniciarSimulacion([7,5,7,9,6,37,11,7,14],"simulacion2.csv")
iniciarSimulacion([9,6,9,11,7,17,13,12,3],"simulacion3.csv")
iniciarSimulacion([15,9,19,17,14,3,19,13,6],"simulacion4.csv")
iniciarSimulacion([19,16,5,21,18,7,23,19,9],"simulacion5.csv")
iniciarSimulacion([25,22,11,27,23,13,29,24,15],"simulacion6.csv")
iniciarSimulacion([31,25,17,33,26,19,35,27,21],"simulacion7.csv")
iniciarSimulacion([37,28,23,39,29,25,41,30,27],"simulacion8.csv")
iniciarSimulacion([43,31,29,45,32,31,47,33,35],"simulacion9.csv")
iniciarSimulacion([49,34,37,51,35,41,53,36,43],"simulacion10.csv")
