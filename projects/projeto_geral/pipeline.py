from pandas import date_range

from src.infra.io.paths import raw_data_file_path, stagging_data_file_path, curated_data_file_path, logs_data_file_path
from src.infra.io.readers import ler_csv_clinte_para_df
from src.infra.io.writers import salvar_df_para_csv
from src.pipelines.auto.basic_pipeline import basic_pipeline_1st, basic_pipeline_2st
from src.pipelines.auto.text_pipeline import text_names_part_one_pipeline, text_basic_pipeline, \
    text_names_part_two_pipeline, text_names_part_tree_pipeline


## Inputs
# Paths
file_name = "projeto_teste.csv"
final_name = "projeto_teste_RevA.csv"
input_file_path = raw_data_file_path(file_name)
curated_file_path = curated_data_file_path(final_name)
logs_file_path = logs_data_file_path("projeto_teste_logs_names.csv")
staging_file_path = stagging_data_file_path("projeto_teste_stagging.csv")



# collumns names
strings_collumns = ["nome", "status"]
email_column = "email"
date_column = "data_nascimento"
nome_column = "nome"
cpf_column = "cpf"
telefone_column = "telefone"


# df
df = ler_csv_clinte_para_df(input_file_path)

# basic cleaning
df = basic_pipeline_1st(df, coluna_data=date_column)



pass

# text basic
df = text_basic_pipeline(df, columns_strings=strings_collumns,
                         column_email=email_column,
                         column_name=nome_column,
                         column_cpf=cpf_column,
                         column_tel=telefone_column)

pass

# limpesa de nomes todo o processo
df = text_names_part_one_pipeline(df, nome_column)
# path do logs
# df = text_names_part_two_pipeline(df, coluna_nome="nome", logs_file_dir=logs_file_path)
pass
df = text_names_part_tree_pipeline(df, coluna_nome=nome_column, path_logs=logs_file_path)

pass



# Limpeza final (tratamento de nulos)
df = basic_pipeline_2st(df)

# Exportar para o Stagging
salvar_df_para_csv(df, staging_file_path)

# Caso queira fazer aplicações mais especificas
'''
Criação de novas categorias, cruzamento de dados, novas colunas
'''

# Exportar versão final para o curated
salvar_df_para_csv(df, curated_file_path)
pass
