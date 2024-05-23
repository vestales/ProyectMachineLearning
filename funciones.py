def eliminar_palabras(text, palabras):
    #Introducimos un texto y una lista de palabras y si el texto se encuentra dentro
    #de la lista lo sustituimos por un espacio.
    for palabra in palabras:
        text = text.replace(palabra, "")
    
    return text.strip()


def modificar_palabras(text, palabras_mod):
    #modificamos las palabras y luego las reemplazamos.
    for palabra, modificar in palabras_mod.items():
        text = text.replace(palabra, modificar)
    
    return text.strip()

def Grafico_trabajo(df):
    import matplotlib.pyplot as plt
    #creamos un gráfico para seleccionar la proporción que queremos de los titulos de trabajos.
    # Sorting the dataframe by proportion in descending order
    df_grafic = df.sort_values(by='proportion', ascending=False).reset_index(drop=True)

    # Calculating the cumulative sum of the proportions
    df_grafic['cumulative_sum'] = df_grafic['proportion'].cumsum()

    # Identifying the threshold index for the cumulative sum of 80%
    threshold_index = df_grafic[df_grafic['cumulative_sum'] <= 0.95].index[-1] + 1

    # Plotting the Pareto chart
    fig, ax1 = plt.subplots(figsize=(20, 6))

    # Plotting the bar chart
    ax1.bar(df_grafic['job_title_clean'], df_grafic['proportion'], color='C0')
    ax1.set_xlabel('Job Titles')
    ax1.set_ylabel('Proportion')
    ax1.tick_params(axis='x', rotation=90)

    # Plotting the cumulative percentage line
    ax2 = ax1.twinx()
    ax2.plot(df_grafic['job_title_clean'], df_grafic['cumulative_sum'], color='C1', marker='o', ms=4)
    ax2.axhline(y=0.95, color='gray', linestyle='--')
    ax2.set_ylabel('Cumulative Proportion')

    # Highlighting the threshold point
    ax2.axvline(x=threshold_index - 1, color='gray', linestyle='--')

    plt.title('Pareto Chart of Job Titles')
    plt.show()
    return df_grafic
    

""" import yaml

    try:
        with open(r"config.yaml", 'r') as file:
            config = yaml.safe_load(file) 
    except Exception as e:
        print(f"Error reading the config file: {e}")

    #leemos la base de datos
    df = pd.read_csv(config['data']['data'])"""

def cargar_y_limpiza_datos():
    import pandas as pd
    url = 'salaries _2.csv'
    df = pd.read_csv(url)

    df = df.drop(columns=["salary_currency", "salary"])

    palabras_eliminar_trabajos = ["Manager", "Specialist", "Lead", "Director", "of",
                                   "Principal", "Managing", "Staff", "AWS", "Associate",
                                     "CRM", "Applied", "Head", "Quantitative", "Cloud",
                                       "Financial", "Marketing", "Compliance"]
    
    #Eliminamos la lista de palabras.
    df["job_title_clean"] = df.job_title.apply(lambda x : eliminar_palabras(x, palabras_eliminar_trabajos))

    #Creamos una lista de las palabras modificadas.
    palabras_mod = {"Science": "Scientist", "Analytics": "Analyst"}  

    #Modificamos las palabras.
    df["job_title_clean"] = df.job_title_clean.apply(lambda x : modificar_palabras(x, palabras_mod))

    #Creamos una tabla con los nombres de los trabajamos ya limpio.
    df_prueba = pd.DataFrame(data= pd.DataFrame(df.job_title_clean.value_counts(normalize=True), 
                                                columns=["proportion"]).values, columns=["proportion"], 
                                                index=[pd.DataFrame(df.job_title_clean.value_counts(normalize=True), 
                                                                    columns=["proportion"]).index])


    #Sustituimos la antigua columna por la nueva ya limpia.
    df["job_title"] = df["job_title_clean"]
    df = df.drop(columns="job_title_clean")

    df_grafic = Grafico_trabajo(df_prueba)

    Lista_trabajos = df_grafic[df_grafic['cumulative_sum'] <= 0.95]["job_title_clean"]

    #Solo dejamos los primeros 95% de datos
    df = df[df.job_title.isin(Lista_trabajos)]

    #Cambiamos los niveles de experiencia de categoricos a numericos.
    palabras_mod = {"EN": "0", "MI": "1", "SE": "2", "EX": "3"}
    df["experience_level"] = df.experience_level.apply(lambda x : modificar_palabras(x, palabras_mod))
    df["experience_level"] = df.experience_level.astype(int)

    #Cambiamos los tamaños de las compañias de categoricos a numericos.
    palabras_mod = {"S": "0", "M": "1", "L": "2"}
    df["company_size"] = df.company_size.apply(lambda x : modificar_palabras(x, palabras_mod))
    df["company_size"] = df.company_size.astype(int)

    #Utilizamos get_dummies en las 3 columnas ya limpiadas.
    df_dummies = pd.get_dummies(df, dtype=int, columns=["employment_type", "job_title", "company_location"])

    #Eliminamos la columna 'employee_residence'.
    df_dummies = df_dummies.drop(columns="employee_residence")

    return df, df_dummies


def grafico_trabajos_salarios_tipos(df):
    import plotly.express as px
    #Creamos un gráfico de cajas entre los titulos de trabajos, salarios y tipos de trabajo.
    fig = px.box(df, x="job_title", y="salary_in_usd", color="employment_type")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.show()

def grafico_remoto_salarios_tipos(df):
    import plotly.express as px
    #Creamos un gráfico de cajas con tipos de trabajo, salarios y ratio en remoto.
    fig = px.box(df, x="employment_type", y="salary_in_usd", color="remote_ratio")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.show()

def grafico_experiencia_salarios_tipos(df):
    import plotly.express as px
    #Creamos un gráfico de cajas entre tipo de trabajo, salarios y nivel de experiencia.
    fig = px.box(df, x="employment_type", y="salary_in_usd", color="experience_level")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.show()

def grafico_remoto_salarios_tamanyo(df):
    import plotly.express as px
    #Creamos un gráfico de cajas entre, nivel de experiencia, salarios y tamaños de las empresas.
    fig = px.box(df, x="experience_level", y="salary_in_usd", color="company_size")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.show()

def grafico_anyos_salarios_experiencia(df):
    import plotly.express as px
    #Creamos un gráfico de cajas entre años, salarios y nivel de experiencia.
    fig = px.box(df, x="work_year", y="salary_in_usd", color="experience_level")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.show()

def grafico_localizacion_salarios_tamanyo(df):
    import plotly.express as px
    #Creamos un gráfico de cajas entre localización de las empresas, salarios y tamaños de éstas.
    fig = px.box(df, x="company_location", y="salary_in_usd", color="company_size")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.show()

def grafico_localizacion_salarios_experiencia(df):
    import plotly.express as px
    #Creamos un gráfico de cajas entre localización de las empresas, salarios y nivel de experiencia.
    fig = px.box(df, x="company_location", y="salary_in_usd", color="experience_level")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.show()


def machine_learning(df):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    import pandas as pd

    #eliminamos la columna 'salary_in_usd' de los features y lo colocamos como target.
    features = df.drop(columns = "salary_in_usd")
    target = df["salary_in_usd"]

    #Separamos la data.
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size = 0.20, random_state=0)

    # Normalize the data
    normalizer = MinMaxScaler()
    X_train_normalized = normalizer.fit_transform(X_train)
    X_test_normalized = normalizer.transform(X_test)

    # Standardize the data
    scaler = StandardScaler()
    X_train_standardized = scaler.fit_transform(X_train)
    X_test_standardized = scaler.transform(X_test)

    gb_reg = GradientBoostingRegressor(max_depth=20,
                                   n_estimators=100)
    
    gb_reg.fit(X_train_normalized, y_train)

    pred = gb_reg.predict(X_test_normalized)

    mae_normalized = mean_absolute_error(pred, y_test)
    mse_normalized = mean_squared_error(pred, y_test, squared=False)
    r2_normalized = gb_reg.score(X_test_normalized, y_test)

    gb_reg = GradientBoostingRegressor(max_depth=20,
                                   n_estimators=100)
    
    gb_reg.fit(X_train, y_train)

    pred = gb_reg.predict(X_test)

    mae_non_transformed = mean_absolute_error(pred, y_test)
    mse_non_transformed = mean_squared_error(pred, y_test, squared=False)
    r2_non_transformed = gb_reg.score(X_test, y_test)

    gb_reg = GradientBoostingRegressor(max_depth=20,
                                   n_estimators=100)
    
    gb_reg.fit(X_train_standardized, y_train)

    pred = gb_reg.predict(X_test_standardized)

    mae_standardized = mean_absolute_error(pred, y_test)
    mse_standardized = mean_squared_error(pred, y_test, squared=False)
    r2_standardized = gb_reg.score(X_test_standardized, y_test)

    results = {
        'Data Transformation': ['Non-Transformed', 'Standardized', 'Normalized'],
        'MSE': [mse_non_transformed, mse_standardized, mse_normalized],
        'MAE': [mae_non_transformed, mae_standardized, mae_normalized],
        'R^2': [r2_non_transformed, r2_standardized, r2_normalized]
    }
    results_df = pd.DataFrame(results)

    return results_df