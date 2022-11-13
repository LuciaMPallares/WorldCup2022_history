#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

import warnings
warnings.filterwarnings('ignore')



def horarios(partidos):
#Ahora separamos todo lo que nos interesa de cada linea y lo guardamos en lista
    ''' Devuelve los datos obtenidos del 
                    web scraping sobre calendario de partidos del mundial: grupo,fecha, equipo local y 
                    y equipo visitante. Una vez obtenidos los datos y separados en listas, crea un diccionario
                    con el nombre de las columnas y almacena los datos en un dataframe'''
    lista =[]
    for i in range(len(partidos)):
        lista.append(partidos[i].text.split('\n'))


#Tenemos una lista de listas con toda la info separada por comas dentro de listas y vamos a extraerlas en simplemente una lista para cada información que queremos.
#Una para Grupos, otra para fecha, para local y para visitante
    grupos=[]
    for i in range(len(lista)):
        if lista[i][0]!='': 
                grupos.append(lista[i][0])

#-----------------------------------
    fecha=[]
    for i in range(len(grupos)):
        fecha.append(lista[i][1])
#Algunas filas contienen día y fecha. Y solo quiero la fecha.
    for i in range(len(fecha)):
        fecha[i]=fecha[i].split(',')[-1]


#-------------------------------------
    local=[]
    for i in range(len(grupos)):
        local.append(lista[i][4])

#-------------------------------------
    visitante=[]
    for i in range(len(grupos)):
        visitante.extend(lista[i][5])
#Una vez están las listas se hace un diccionario para que sea más cómodo crear la tabla
    worldcup = {'Fecha': fecha,
            'Local': local,
            'Visitante': visitante,
            'Grupo': grupos}

#Transformar el diccionario en un dataFrame y se retorna.
    worldcup_df=pd.DataFrame(worldcup)
    print(worldcup_df.tail(40))
    return worldcup_df

#Funcion llamada dentro de Padre. Te compara el gol de equipo 1 con equipo 2 y te devuelve si gana equipo 1 equipo 2 o es empate(tie)
def result(row):
    '''Compara el número de goles del equipo 1 con el equipo 2 y te devuelve el nombre del equipo 
                     que tiene un número de goles mayor, o si es empate(tie) '''

    if row["Home Team Goals"] > row["Away Team Goals"]:
      return row["Home Team Name"]
    elif row["Away Team Goals"] > row["Home Team Goals"]:
      return row['Away Team Name']
    else:
      return 'Tie' 

    
#Funcion llamada en 'lastmatches' que nos va a crear una lista de todos los partidos de 'last matches'(5 ultimos) separadas por el atributo que le pidamos en forma de int.
def relleno(attr, datos):
    ''' Obtiene los datos de una lista de tuplas y los guarda en una lista
                             para poder trabajar con ellos separadamente.'''
    lista=[]
    for e in datos:
        lista.append(e[attr])
    
    return lista
        
#Te da un listado con todos los partidos entre equipo1 y equipo2
def matches(pais1, pais2):
    '''Devuelve un listado con todos los partidos jugados entre el
                               equipo del pais1 y el equipo del pais2. De la base de datos
                               WorldCupMatches obtiene los datos, borra duplicados, fila y columnas no 
                               necesarias,cambia 3 columnas de tipo float a int. Crea columna Winner llamando 
                               a la función result incluida en este documento. Finalmente recorre la tabla con 
                               las estadísticas de los encuentros jugados por todos los partidos y devuelve una lista
                               con año, goles y ganador de los dos equipos que se introduzcan en la función.'''
    
    #Leemos WorldCupMatches y lo modificaremos------------------------------------
    partidos=pd.read_csv('WorldCupMatches.csv')
    #Borrado de duplicados
    partidos.drop_duplicates(inplace=True)
    #Borramos las columnas que no nos interesan
    col=['Datetime', 'Stage', 'City', 'Win conditions', 'Attendance', 'Half-time Home Goals',
       'Half-time Away Goals', 'Referee', 'Assistant 1', 'Assistant 2',
       'RoundID', 'MatchID', 'Home Team Initials', 'Away Team Initials']
    partidos.drop(columns = col, axis=1, inplace = True)
    #Y una fila vacía, la 852
    partidos.drop([852],axis=0, inplace=True)
    #Las columnas float las cambiamos a int
    partidos["Home Team Goals"]= partidos["Home Team Goals"].astype('int32') 
    partidos["Year"]=partidos["Year"].astype('int')
    partidos["Away Team Goals"]= partidos["Away Team Goals"].astype('int32')
    #Reiniciamos Index
    partidos.reset_index(drop=True)
    #-----------------------------------------------------------------------------------------------
    #Creamos la comuna Winner que se rellena con equipo 1 equipo 2 o tie usando la función antes definida "result"
    partidos["Winner"] = partidos.apply(lambda row: result(row), axis=1)

    #Creamos la lista vacía llamada "prueba" para rellenarla con solo las estadisticas de pais1 y pais2
    prueba=[]
    for e in range(len(partidos)):
        if (partidos["Home Team Name"][e] == pais1 and partidos['Away Team Name'][e]== pais2) | (partidos["Away Team Name"][e] == pais1 and partidos["Home Team Name"][e] == pais2):
            prueba.append(((((((partidos["Year"][e], partidos["Home Team Name"][e], partidos["Home Team Goals"][e], partidos["Away Team Name"][e], partidos["Away Team Goals"][e], "winner-->", partidos["Winner"][e])))))))
     
    return prueba


#Crea una tabla (DataFrame) con los resultados de los últimos 5 partidos
def lastmatchs(equipo1,equipo2):
    '''Devuelve un DataFrame con los resultados de los últimos 5 partidos de los dos 
                            equipo que se introducen en la función. Para ellos llamamos a la función matches 
                            que nos dará todos los datos de los enfrentamientos de esas dos selecciones, selecciona
                            las posiciones donde están los datos requeridos y crea 6 variables con el nombre de 
                            las columnas para devolver el DF'''
    #Rellenamos datos con los ultimos partidos entre las 2 selecciones
    datos=matches(equipo1,equipo2)
    #Tomamos los 5 ultimos
    datos=datos[-5:]
    #Rellenamos una variable por atributo donde hay una lista de ese atributo muchas veces.Me cansa escribir.
    año= relleno(0, datos)
    loc= relleno(1, datos)
    gloc= relleno(2, datos)
    vis= relleno(3, datos)
    gvis= relleno(4, datos)
    gan= relleno(6, datos)
    #Con las listas antes creadas formammos un Super DATAFRAME
    lm=pd.DataFrame()
    lm['Year']= año
    lm['Home Team Name']= loc
    lm['Home Team Gol']= gloc
    lm['Away Team Name']= vis
    lm['Away Team Gol']= gvis
    lm['Winner']= gan
    
    
    return lm



def queen(pais1,pais2):
    #Llamando a la función historial obtendremos una lista con el palmarés de cada país.([0]-wins,  [1]-seconds, [2] thirds.)
    '''Define dos variables con el palmarés de títulos obtenidos en el mundial por el pais1 y pais2,
                                    llama a la función match para obtener los datos de los enfrentamientos entre esos dos partidos,
                                    llama a función relleno para trabajar separadamente con los datos almacenados en hist y con un contador
                                    almacena en 3 variables las victorias de cada país, y los empates. Creación de un Dataframe con todos los
                                    datos recogido'''
    pais1_wins=historial(pais1)
    pais2_wins=historial(pais2)
    hist=matches(pais1,pais2)#papa
    winns=relleno(6,hist)
    victorias_pais1=winns.count(pais1)
    victorias_pais2=winns.count(pais2)
    empates=winns.count('Tie')

    #Creamos el DataFrame con toda la información  
    reina=pd.DataFrame()
    paises=[pais1,pais2]
    wins1=[victorias_pais1,victorias_pais2]
    draws=[empates,empates]
    loses=[victorias_pais2,victorias_pais1]
    wc_1=[pais1_wins[0],pais2_wins[0]]
    wc_2=[pais1_wins[1],pais2_wins[1]]
    wc_3=[pais1_wins[2],pais2_wins[2]]
    reina['Country']= paises
    reina['Wins']= wins1
    reina['Draws']= draws
    reina['Loses']= loses
    reina['World Cup 1st']=wc_1
    reina['World Cup 2nd']=wc_2
    reina['World Cup 3rd']=wc_3
    return reina


    #-------------------------------------------------
def historial(pais):
    '''Devuelve una lista con el número total de títulos obtenidos en primer, segundo,
                    y tercer puesto. Para ello realiza un contador de cada columna por cada país
                    de la la base de datos WorldCups, corregido error si no ha obtenido ningun 
                    título en alguna categoría. Se unifica el nombre de Germany eliminando el FR. '''
        
    mundiales = pd.read_csv('WorldCups.csv')
    #Vamos a cambiar todos los 'Germany FR' por 'Germany'
    for i in range(len(mundiales)):
        if mundiales['Winner'][i] == 'Germany FR':
            mundiales['Winner'][i] = 'Germany'
        if mundiales['Runners-Up'][i] == 'Germany FR':
            mundiales['Runners-Up'][i] = 'Germany'
        if mundiales['Third'][i] == 'Germany FR':
            mundiales['Third'][i] = 'Germany'
        if mundiales['Fourth'][i] == 'Germany FR':
            mundiales['Fourth'][i] = 'Germany'
    #Contabilizador de titulos       
    pos1 = mundiales['Winner'].value_counts()
    pos2 = mundiales['Runners-Up'].value_counts()
    pos3 = mundiales['Third'].value_counts()
    #Hacemos un try porque si no está en pos es que nunca ha ganado nada y es remalo.
    try:
        pos_1 = pos1[pais]
    except:
        pos_1 = 0
    try:
        pos_2 = pos2[pais]
    except:
        pos_2 = 0
    try:
        pos_3 = pos3[pais]
    except:
        pos_3 = 0
    lista=[pos_1,pos_2,pos_3]
    return lista 

#Diccionario Magic English
def eng(pais):
    '''Creación de un diccionario con el nombre de los países traducidos al inglés,
                     si el usuario introduce el nombre del país en español lo busca en inglés.'''
        
    countrys={'Ecuador':'Ecuador',
 'Ghana':'Ghana',
 'Polonia':'Poland',
 'Canadá':'Canda',
 'Serbia':'Serbia',
 'Australia':'Australia',
 'Japón':'Japan',
 'Senegal':'Senegal',
 'México':'Mexico',
 'España':'Spain',
 'Croacia':'Croatia',
 'Francia':'France',
 'Bélgica':'Belgium',
 'Camerún':'Cameroon',
 'Uruguay':'Uruguay',
 'Arabia Saudita':'Saudi Arabia',
 'Catar':'Qatar',
 'Estados Unidos':'USA',
 'Gales':'Wales',
 'Portugal':'Portugal',
 'Dinamarca':'Denmark',
 'Argentina':'Argentina',
 'Inglaterra':'England',
 'Corea del Sur':'South Korea',
 'Suiza':'Switzeland',
 'Túnez':'Tunisia',
 'Brasil':'Brazil',
 'Paises Bajos':'Netherlands',
 'Irán':'Iran',
 'Costa Rica':'Costa Rica',
 'Alemania':'Germany',
 'Marruecos':'Morocco'}

    try:
        respuesta=countrys[pais]
    except:
        respuesta=pais
    return respuesta

    


# %%
