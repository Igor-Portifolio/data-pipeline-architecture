from src.infra.io.paths import raw_data_file_path, staging_data_file_path, curated_data_file_path, logs_data_file_path
from src.infra.io.readers import read_client_csv_to_dataframe
from src.infra.io.writers import save_dataframe_to_csv
from src.pipelines.sanitization import full_sanitization, final_null_normalization
from src.pipelines.text_processing import text_normalization_and_validation, proper_name_apply_review_log

## Inputs
# Paths
file_name = "projeto_teste.csv"
final_name = "projeto_teste_RevA.csv"
input_file_path = raw_data_file_path(file_name)
curated_file_path = curated_data_file_path(final_name)
logs_file_path = logs_data_file_path("projeto_teste_logs_names.csv")
staging_file_path = staging_data_file_path("projeto_teste_stagging.csv")

# collumns names
strings_collumns = ["nome", "status"]
email_column = "email"
date_column = "data_nascimento"
nome_column = "nome"
cpf_column = "cpf"
telefone_column = "telefone"

# df
df = read_client_csv_to_dataframe(input_file_path)
df = full_sanitization(df, column_date=date_column)
df = text_normalization_and_validation(df, columns_strings=strings_collumns,
                                       column_email=email_column,
                                       column_name=nome_column,
                                       column_cpf=cpf_column,
                                       column_tel=telefone_column)
df = proper_name_apply_review_log(df, column_name=nome_column, logs_file_dir=logs_file_path)
df = final_null_normalization(df)
save_dataframe_to_csv(df, staging_file_path)
save_dataframe_to_csv(df, curated_file_path)
