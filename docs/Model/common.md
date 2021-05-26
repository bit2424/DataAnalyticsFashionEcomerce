# Help on module common:

### NAME
    common

## CLASSES
    builtins.object
        Commons
        pcolors
    
    class Commons(builtins.object)
     |  Static methods defined here:
     |  
     |  append_tags_analysis_columns(df, df_interesting, col)
     |      En esta parte agregaremos 2 columnas que se relacionan con los tags:
     |      *   best_tag_units_sold: Escogemos el valor del tag con las mejores ventas promedio
     |      *   Elemento de lista: Calculamos el promedio del promedio de las ventas de todos los tag
     |      
     |      El primer paso es crear un diccionario con todas los precios de los productos que tienen un tag especifico.
     |      
     |      :param df: El dataframe original
     |      :param df_interesting: El dataframe con las caracteristicas de interes
     |      :param col: La columna de interes de los dataframe
     |      :return: Los dataframes recibidos por parametro modificados con las nuevas columnas
     |  
     |  clean(df)
     |      Realiza limpieza de datos sobre el dataframe pasado por parametro. No hay valor de retorno ya que la limpieza se hace *in place*.
     |      
     |      :param df: El dataframe de pandas sobre el que se hará limpieza
     |  
     |  extract_interesting_features(df, type)
     |      Extrae las caracteristicas más importantes del dataframe para el modelo seleccionado por parametro.
     |      
     |      :param df: El dataframe del que se extraeran caracteristicas
     |      :param type: La caracteristica base que identifica al modelo que extrae las caracteristicas
     |      :return: un dataframe de pandas con las caracteristicas más interesantes dependiendo del modelo
     |  
     |  one_hot_encode(df)
     |      Ahora realizaremos una codificación onehot, para convertir todas las variables categoricas en varias columnas de valores enteros binarios.
     |      
     |      :param df: El dataframe de pandas sobre el que se hará la codificación *one-hot*
     |      :return: El dataframe codificado
     |  
     |  plot_colors_vs_feature(df, feature)
     |  
     |  plot_missing_data(df)
     |      Grafica con seaborn la cantidad de nans por columna del dataframe pasado por parametro.
     |      
     |      :param df: El dataframe de pandas sobre el que se hará la grafica de nans
     |  
     |  print_correlation_map(df, col)
     |      Se imprime la matriz de correlación para la caracteristica seleccionada por parametro.
     |      
     |      :param df: El dataframe sobre el que se hace la matriz de correlación
     |      :param col: La columna del dataframe que se analizará
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class pcolors(builtins.object)
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  BOLD = '\x1b[1m'
     |  
     |  ENDC = '\x1b[0m'
     |  
     |  FAIL = '\x1b[91m'
     |  
     |  HEADER = '\x1b[95m'
     |  
     |  OKBLUE = '\x1b[94m'
     |  
     |  OKCYAN = '\x1b[96m'
     |  
     |  OKGREEN = '\x1b[92m'
     |  
     |  UNDERLINE = '\x1b[4m'

FILE
> [Model/common.py](../../Model/common.py)


