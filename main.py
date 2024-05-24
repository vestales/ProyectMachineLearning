from funciones import cargar_y_limpiza_datos, grafico_trabajos_salarios_tipos, grafico_remoto_salarios_tipos,\
                    grafico_experiencia_salarios_tipos, grafico_remoto_salarios_tamanyo,grafico_anyos_salarios_experiencia,\
                    grafico_localizacion_salarios_tamanyo, grafico_localizacion_salarios_experiencia, machine_learning

df, df_dummies = cargar_y_limpiza_datos()

grafico_trabajos_salarios_tipos(df)

grafico_remoto_salarios_tipos(df)

grafico_experiencia_salarios_tipos(df)

grafico_remoto_salarios_tamanyo(df)

grafico_anyos_salarios_experiencia(df)

grafico_localizacion_salarios_tamanyo(df)

grafico_localizacion_salarios_experiencia(df)

resultado = machine_learning(df_dummies)

print(resultado)