# <h1 align=center> **Proyecto Individual MLOps** </h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>
<p align="center">
¡Bienvenidos a mi primer proyecto individual de la etapa de labs!

<hr>  

## **Descripción del problema (Contexto y rol a desarrollar)**

Trabajo como **`Data Scientist`** en una start-up que provee servicios de agregación de plataformas de streaming. Creo mi primer modelo de ML: un sistema de recomendación de peliculas, basada en el tipo de contenido. 

Se me pide un trabajo rápido de **`Data Engineer`** y tener un **`MVP`** (_Minimum Viable Product_)

## **Proyecto**

**`Transformaciones realizadas`**: [ETL Plataformas](https://github.com/laumaita/PI01_HENRY-09/blob/main/transformacion_datos_plataformas.ipynb) , [ETL Rating](https://github.com/laumaita/PI01_HENRY-09/blob/main/transformacion_ratings.ipynb)

**`Análisis exploratorio de datos`**: [EDA](https://github.com/laumaita/PI01_HENRY-09/blob/main/EDA.ipynb)

**`API`**: [Deploy](https://pi01-henry-09.onrender.com/docs) (Propuesta para disponibilizar los datos de la empresa con el framework ***FastAPI***)

En esta propuesta se realizaron 6 endpoints, para consultar: 

+ get_max_duration = Indica la pelicula con mayor duracion, segun la plataforma y el año dado
+ get_score_count = Cantidad de películas según plataforma, con un puntaje mayor a XX en determinado año.
+ get_count_platform = Cantidad de películas según plataforma(netflix, amazon, hulu, disney)
+ get_actor = Actor que más se repite según plataforma y año. 
+ prod_per_county = La cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año.
+ get_contents = La cantidad total de contenidos/productos (todo lo disponible en streaming, series, peliculas, etc) según el rating de audiencia dado (para que publico fue clasificada la pelicula). 
+ get_recommendation = Recomienda 5 peliculas, segun las caracteristicas de la pelicula ingresada.

**`Sistema de recomendación`**: [ML](https://github.com/laumaita/PI01_HENRY-09/blob/main/ML_sistema_recomendacion.ipynb) 

