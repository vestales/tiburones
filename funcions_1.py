def Cargar_datos(url):
    import pandas as pd
    """
        - Cargamos el dataframe y desplegamos todas las columnas
        - Formateamos el nombre de las columnas poniendo todos los caracteres en minúscula, reemplazando los espacios y los puntos por '_' y los ':' por espacio.
        - Eliminamos las columnas que no necesitamos para el objetivo del proyecto
    """
    
    df = pd.read_excel(url)

    pd.set_option("display.max_columns",None)

    df.columns = df.columns.str.lower().str.strip().str.replace(" ","_").str.replace(".","_").str.replace(":","")

    df.drop(["unnamed_11", "unnamed_21", "unnamed_22", "case_number_1", "case_number", "href", "href_formula", "pdf", "original_order", "source"], axis = 1, inplace = True)

    """
        Aqui lo que hacemos es cambiar todas las fechas a un formato apto para 'date'.

        Por lo tanto lo primero que hacemos es cambiar los meses a numero y quitar los guiones por espacios.

        Luego los tranformamos en formato 'date' en una nueva columna llamada 'date_clean'
        y en las filas que no se han cambiado las eliminamos ya que con esas filas no podemos trabajar
        que en total han sido unas 1000 de 4810(entre esas filas que hemos eliminado han sido las que no tenian dia o mes).

        Finalmente hemos pasado las fechas de 'date_clean' a 'date' y hemos eliminado 'date_clean'.
    """

    date_values_combine = {
        "Jan" : "01",
        "Feb" : "02",
        "Mar" : "03",
        "Apr" : "04",
        "May" : "05",
        "Jun" : "06",
        "Jul" : "07",
        "Aug" : "08",
        "Sep" : "09",
        "Oct" : "10",
        "Nov" : "11",
        "Dec" : "12"
    }

    for nombre, numero in date_values_combine.items():
        df["date"] = df["date"].str.replace(nombre, numero)


    df["date"] = df["date"].str.replace("-", " ")

    df["date_clean"] = pd.to_datetime(df["date"], format="%d %m %Y", errors='coerce')

    df = df.dropna(subset=["date_clean"])

    df["date"] = df["date_clean"]

    df = df.drop(columns = ["date_clean"])


    """ limpiamos 'type':
      - Creamos un nuevo diccionario con los nuevos valores para 'type"
      - Reemplazamos los nuevos valores en la columna
      - Creamos una lista con los valores que nos queremos quedar
      - Actualizamos la columna solo con los valores que queremos
    """
    type_values_combine = {
        " Provoked" : "Provoked",
        "Boat" : "Watercraft"
    }

    df["type"] = df["type"].replace(type_values_combine)

    type_list = ["Unprovoked", "Provoked", "Watercraft"]

    df = df[df["type"].isin(type_list) == True]

    #limpiamos el género, actividades, nombres, country, state, location, injury y species:

    sex_values_combine = {
        " M" : "M",
        "M " : "M"
    }

    df["sex"] = df["sex"].replace(sex_values_combine)

    df["activity"] = df["activity"].str.strip().str.replace(",","").str.split(" ").str[0]

    df["name"] = df["name"].str.strip()

    df["country"] = df["country"].str.strip().str.title()

    df["state"] = df["state"].str.strip()

    df["location"] = df["location"].str.strip()

    df["injury"] = df["injury"].str.strip()

    df["species"] = df["species"].str.strip().str.replace('"', "")

    """ Vamos a reducir los datos a los ultimos 10 años.
        -creamos una lista con los años deseados y solo dejamos los datos de esos años.
    """

    year_valid = []
    actual_year = 2024
    for x in range(10):
        y = actual_year-x
        year_valid.append(y)

    df = df[df["year"].isin(year_valid) == True]

    #creamos dos columnas nueva una para dias de la semana y otra para mes

    df['week_day'] = df['date'].dt.day_name(locale='')

    df['month'] = df['date'].dt.month

    return df




def graf_ataques_ciudad(df):
    import pandas as pd
    import  plotly.express  as  px 


    ataques_ciudad = df.groupby(['country', 'state'])["date"].agg('count').reset_index().rename(columns={'date': 'atack'})

    ataques_ciudad = ataques_ciudad.sort_values(by = 'atack', ascending=False)

    ataques_ciudad = ataques_ciudad.head(int(len(ataques_ciudad) * 0.1))
    fig = px.pie(ataques_ciudad, values='atack', names='state', title='Attack of shark in different states')
    fig.show()


def graf_ataques_especies(df):
    import seaborn as sns
    import matplotlib.pyplot as plt

    ataques_especies = df.groupby(['species'])["date"].agg('count').reset_index().rename(columns={'date': 'atack'})

    ataques_especies = ataques_especies.sort_values(by = 'atack', ascending=False)

    ataques_especies = ataques_especies.head(int(len(ataques_especies) * 0.1))
    ax = sns.barplot(x = "species",y = "atack", data= ataques_especies)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

    plt.show()


def graf_barra_ataques_ciudad_mes(df):
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    ataques_ciudad = df.groupby(['country', 'state'])["date"].agg('count').reset_index().rename(columns={'date': 'atack'})

    ataques_ciudad = ataques_ciudad.sort_values(by = 'atack', ascending=False)

    ataques_ciudad = ataques_ciudad.head(int(len(ataques_ciudad) * 0.1))

    top_states = list(ataques_ciudad['state'])

    ataques_ciudad_con_mes = df.groupby(['country', 'state', 'month'])["date"].agg('count').reset_index().rename(columns={'date': 'atack'})

    ataques_ciudad_con_mes = ataques_ciudad_con_mes.sort_values(by = 'atack', ascending=False)
    ataques_ciudad_con_mes = ataques_ciudad_con_mes[ataques_ciudad_con_mes.state.isin(top_states)]

    import matplotlib.pyplot as plt


    sns.set_theme(style="darkgrid")

    plt.figure(figsize=(20, 10))  # Por ejemplo, 12 pulgadas de ancho por 6 de alto

    # Plot the responses for different events and regions
    sns.lineplot(x="month", y="atack",
                hue="state", style="country",
                data=ataques_ciudad_con_mes)
    
    

def graf_cir_ataques_ciudad_mes(df):
    import pandas as pd
    import  plotly.express  as  px 

    ataques_ciudad = df.groupby(['country', 'state'])["date"].agg('count').reset_index().rename(columns={'date': 'atack'})

    ataques_ciudad = ataques_ciudad.sort_values(by = 'atack', ascending=False)

    ataques_ciudad = ataques_ciudad.head(int(len(ataques_ciudad) * 0.1))

    top_states = list(ataques_ciudad['state'])

    ataques_ciudad_con_mes = df.groupby(['country', 'state', 'month'])["date"].agg('count').reset_index().rename(columns={'date': 'atack'})

    ataques_ciudad_con_mes = ataques_ciudad_con_mes.sort_values(by = 'atack', ascending=False)
    ataques_ciudad_con_mes = ataques_ciudad_con_mes[ataques_ciudad_con_mes.state.isin(top_states)]



    fig = px.bar(ataques_ciudad_con_mes, x='month', y='atack', color='state',
             hover_data=['country'],
             title='ataques de tiburon por ciudad')
    fig.show()


