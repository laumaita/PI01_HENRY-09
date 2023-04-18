from fastapi import FastAPI
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors


app = FastAPI()

@app.on_event('startup')
def startup():
    global df_plataformagral
    url = 'https://drive.google.com/file/d/1TLLaZFA1-j_lsdY7C8jTc9OkaSeTXEF2/view?usp=share_link'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df_plataformagral =  pd.read_csv(path)

    global df_score
    url2 = 'https://drive.google.com/file/d/1dvoWrjxph3FKBETsbOI_-Vi0wqix_BMr/view?usp=share_link'
    path2 = 'https://drive.google.com/uc?export=download&id='+url2.split('/')[-2]
    df_score= pd.read_csv(path2)

    global df_peliculas
    url3 = 'https://drive.google.com/file/d/1dJeukGQytXkEhhT40EFK_ZxennhbmzsD/view?usp=share_link'
    path3 = 'https://drive.google.com/uc?export=download&id='+url3.split('/')[-2]
    df_peliculas= pd.read_csv(path3)

    global df_filt_peliculas
    url4 = 'https://drive.google.com/file/d/1WPpmgkAAQZrEGIdHOJ1IiDYmnOXj-2aW/view?usp=share_link'
    path4 = 'https://drive.google.com/uc?export=download&id='+url4.split('/')[-2]
    df_filt_peliculas= pd.read_csv(path4)    


@app.get("/")
async def root():
    return {'Proyecto individual 01': "Laura Maita"}

@app.get("/get_max_duration/{anio}/{plataforma}/{dtype}")
def get_max_duration(year:int,platform:str,duration_type:str):
    
    #declaro parametros
    if platform == 'netflix':
        inicioId = 'n'
    elif platform == 'hulu':
        inicioId = 'h'
    elif platform == 'disney':
        inicioId = 'd'
    elif platform == 'amazon':
        inicioId = 'a'
    else:
        return {'error':'no se encuentra plataforma, ingresar una de las opciones: netflix, hulu, disney o amazon'}
    

    if duration_type == 'pelicula':
        durationtype= 'movie' 
    else:
        return {'error':'ingresar parametro : pelicula' }

    filtro = df_plataformagral[ (df_plataformagral.type==durationtype) #filtro por peliculas
                            & (df_plataformagral.id.str.contains(inicioId)) #filtro por primer letra de plataforma
                            & (df_plataformagral.release_year==year)]  #filtro por el año

    max = filtro['duration_int'].max() #guardo el valor maximo
    filtro1 = filtro.query("duration_int==@max") #consulto la duracion de ese valor
    pelicula = filtro1['title'] #guardo lo que quiero que retorne
    if  not pelicula.empty: #si segun los datos ingresados el dataframe no esta vacio
        return {'pelicula': pelicula.iloc[0]}
    else:
        return {'error' : 'El año ingresado no se encuentran en la base de datos'}

@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(platform:str, scored:float, year:int):  

    #declaro parametros
    if platform == 'netflix':
        plataforma = 'n'
    elif platform == 'hulu':
        plataforma = 'h'
    elif platform == 'disney':
        plataforma = 'd'
    elif platform == 'amazon':
        plataforma = 'a'
    else:
        return {'error':'ingresar una de las opciones: netflix, hulu, amazon o disney'}
    
    
    clasificacion = df_plataformagral[ (df_plataformagral.type=='movie')#busco  solo las peliculas
                                        & (df_plataformagral.id.str.contains(plataforma)) #filtro por plataforma
                                        & (df_plataformagral.release_year==year)]  #filtro por el año
                                        

    consulta_score= df_score[(df_score.movieId.str.contains(plataforma))] #filtro por plataforma 
    df_peliculas=consulta_score[consulta_score.movieId.isin(clasificacion.id)]#me quedo solo con los id que estan en ambos df
    total_peliculas = df_peliculas.score[df_peliculas.score >scored].count()#filtro por el puntaje mayor a xx del campo score y cuento los valores totales


    return {'plataforma' : str(platform) , 'cantidad': int(total_peliculas), 'anio' : int(year), 'score' : float(scored)}

@app.get('/get_count_platform/{plataforma}')
def get_count_platform(platform:str): 

    #Declaro parametros
    if platform == 'netflix':
        plataforma = 'n'
    elif platform == 'hulu':
        plataforma= 'h'
    elif platform == 'disney':
        plataforma= 'd'
    elif platform == 'amazon':
        plataforma= 'a'
    else:
        return print('ingrese plataforma: amazon, disney, hulu o netflix')

   

    consulta_plataforma= df_plataformagral[(df_plataformagral.id.str.contains(plataforma))#filtro por plataforma
                                           & (df_plataformagral.type=='movie')]#filtro por peliculas

                                           
    conteo_movies= consulta_plataforma.title.count()#cuento
    return { 'plataforma': str(platform), 'peliculas': int(conteo_movies)}

@app.get('/get_actor/{plataforma}/{anio}')
def get_actor(platform:str, year:int): 

    #declaro parametros
    if platform == 'netflix':
        plataforma= 'n'
    elif platform == 'disney':
        plataforma= 'd'
    elif platform == 'hulu':
        plataforma= 'h'
    elif platform == 'amazon':
        plataforma= 'a'
    else:
        return {'error':'ingresar plataforma valida: amazon, disney, hulu o netflix'}


    filtroplat = df_plataformagral[(df_plataformagral.id.str.contains(plataforma))
                                   & (df_plataformagral.release_year==year)] #filtro por año y plataforma

    if filtroplat.empty: #si devuelve df vacio
        
        return {'error':'el año no se encuentra en el dataset'}
    else:
        lista= filtroplat['cast'] #guardo en nueva variable los actores por peliculas
        newlista = [x for x in lista if pd.isnull(x) == False]#elimino flotantes

        lista_cast=[]
        for i in newlista: #itero para separar actores en diferentes str
            separador= i.split(sep=',')
            for j in separador: #itero para eliminar espacios en cada nuevo str y agregar a lista
                    valores=j.strip()
                    lista_cast.append(valores) #agrego valores a lista_cast
        df_lista_cast= pd.Series(lista_cast) #transformo a dataframe
        actor = df_lista_cast.value_counts().idxmax()
        apariciones= df_lista_cast.value_counts().max()
        return {'plataforma': str(platform), 'anio': int(year), 'actor' : str(actor), 'apariciones' : int(apariciones)} #imprimo copnsulta del str mas repetido

@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo:str,pais:str,anio:int):

    #declaramos parametros
    
    if tipo == 'peliculas' :
        variable_tipo= 'movie'
    elif tipo == 'series':
        variable_tipo= 'tv show'
    else:
        return 'ingresar parametro : peliculas o series'

    filtro=df_plataformagral[(df_plataformagral.type=='movie') 
                                    & (df_plataformagral.release_year==anio)
                                    & (df_plataformagral.country.notnull())
                                    & (df_plataformagral.country.str.contains(pais))]

    respuesta= filtro.type.count()

    return {'pais': str(pais), 'anio': int(anio), 'variable_tipo': int(respuesta)}

@app.get('/get_contents/{rating}')
def get_contents(rating:str):
    
    total_contenido= df_plataformagral.type[df_plataformagral.rating==rating].count()


    if total_contenido == 0 :
        return {'ingresar una de las sigientes categorias ' : '''pg-13', 'tv-ma', 'pg', 'tv-14', 'tv-pg', 'tv-y', 'tv-y7', 'r','tv-g', 'g', 'nc-17', 'nr','tv-y7-fv', 'ur', 'not rated','13+', 'all', '18+','16+', '7+', 'tv-nr', 'unrated', '16','ages_16_', 'ages_18_', 'all_ages', 'not_rate'''}
    else:
        return {'rating': str(rating), 'contenido' : int(total_contenido)}

@app.get('/get_recomendation/{title}')   
def get_recommendation(titulo: str):

    if df_peliculas.title[df_peliculas.title==titulo].empty:
        return 'pelicula no encontrada' 
    else: 
        # Creo pipeline para variables numericas
        pipeline_num = Pipeline([
            ('scaler', StandardScaler())
            ])
        # Creo pipeline para variables categoricas
        pipeline_categorica = Pipeline([
            ('encoder', OneHotEncoder(drop = 'first'))
            ])
        # creo col_transf
        col_transf = ColumnTransformer([
            ('numeric', pipeline_num, df_filt_peliculas._get_numeric_data().columns.tolist()),
            ('categoric', pipeline_categorica, df_filt_peliculas.select_dtypes('object').columns.tolist()) 
            ])
        #entrenamos
        col_transf_fit = col_transf.fit(df_filt_peliculas)
        df_filt_transf = col_transf_fit.transform(df_filt_peliculas)    
        #knn vecinos
        n_neighbors=6
        nneighbors = NearestNeighbors(n_neighbors = n_neighbors, metric = 'cosine').fit(df_filt_transf)
        

        indice=df_peliculas[df_peliculas.title==titulo].index.values[0]#
        dif, ind = nneighbors.kneighbors(df_filt_transf[indice])

        df_peliculas.loc[ind[0][0], :]

        recomendado=df_peliculas.loc[ind[0][1:], :].sort_values('score', ascending=False)
        lista = recomendado.title.to_list()
        return {'recomendacion': lista}

