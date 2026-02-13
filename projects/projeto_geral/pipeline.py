from src.infra.io.paths import *
from src.infra.io.readers import *
from src.infra.io.writers import *

# Paths
file_name = "projeto_teste.csv"
# C:\projetos_solve\scripts_geral\data\raw\client\projeto_teste.csv
file_path = raw_data_file_path(file_name)

pass

# data frame
df = ler_csv_clinte_para_df(file_path)

pass



