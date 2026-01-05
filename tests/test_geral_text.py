'''
def test_create_feedback_file(tmp_path, monkeypatch):
    """
    Testa se:
    - cria a pasta text_files
    - cria o arquivo com nome correto
    - escreve o conteúdo correto
    """

    # Simula:
    # tmp_path/
    #   src/
    fake_src = tmp_path / "src"
    fake_src.mkdir()

    fake_file = fake_src / "geral_text.py"
    fake_file.write_text("# fake file")

    monkeypatch.setattr(
        "src.geral_text.__file__",
        str(fake_file)
    )

    rev = "v1"

    file_path = Standard_text.create_feedback_file(rev)

    expected_folder = tmp_path / "text_files"
    expected_file = expected_folder / "client_feedback_v1.txt"

    assert file_path == expected_file
    assert expected_folder.exists()
    assert expected_file.exists()
    assert expected_file.read_text(encoding="utf-8") == "v1:\n\n"


def test_normalize_nulls_all_columns_to_na():
    df = pd.DataFrame({
        "nome": ["Ana", "", "None"],
        "cidade": ["SP", " ", "nan"]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_nulls()

    assert pd.isna(result.loc[1, "nome"])
    assert pd.isna(result.loc[2, "nome"])
    assert pd.isna(result.loc[1, "cidade"])
    assert pd.isna(result.loc[2, "cidade"])


def test_normalize_nulls_replace_with_text():
    df = pd.DataFrame({
        "nome": ["Ana", "", "nan"]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_nulls(nulo="SEM INFO")

    assert result["nome"].tolist() == ["Ana", "SEM INFO", "SEM INFO"]


def test_normalize_nulls_single_column():
    df = pd.DataFrame({
        "nome": ["Ana", ""],
        "idade": [30, ""]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_nulls(coluna="nome")

    assert pd.isna(result.loc[1, "nome"])
    assert result.loc[1, "idade"] == ""


def test_normalize_nulls_invalid_column_raises():
    df = pd.DataFrame({
        "nome": ["Ana"]
    })

    cleaner = Standard_text(df)

    with pytest.raises(KeyError):
        cleaner.normalize_nulls(coluna="coluna_invalida")


def test_normalize_nulls_preserves_valid_values():
    df = pd.DataFrame({
        "nome": ["Ana", "Bruno"],
        "cidade": ["SP", "RJ"]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_nulls()

    assert result.equals(df)



def test_get_string_columns_basic():
    df = pd.DataFrame({
        "nome": ["Ana", "Bruno"],
        "idade": [30, 40],
        "cidade": ["SP", "RJ"]
    })

    cleaner = Standard_text(df)
    cols = cleaner._get_string_columns()

    assert set(cols) == {"nome", "cidade"}


def test_get_string_columns_string_dtype():
    df = pd.DataFrame({
        "nome": pd.Series(["Ana", "Bruno"], dtype="string"),
        "idade": [25, 35]
    })

    cleaner = Standard_text(df)
    cols = cleaner._get_string_columns()

    assert cols == ["nome"]


def test_get_string_columns_no_string_columns():
    df = pd.DataFrame({
        "idade": [10, 20],
        "ativo": [True, False]
    })

    cleaner = Standard_text(df)
    cols = cleaner._get_string_columns()

    assert cols == []


def test_get_string_columns_empty_dataframe():
    df = pd.DataFrame()

    cleaner = Standard_text(df)
    cols = cleaner._get_string_columns()

    assert cols == []


def test_get_string_columns_does_not_modify_df():
    df = pd.DataFrame({
        "nome": ["Ana"],
        "idade": [30]
    })

    df_original = df.copy(deep=True)

    cleaner = Standard_text(df)
    _ = cleaner._get_string_columns()

    assert cleaner.df.equals(df_original)



def test_normalize_text_only_strip():
    df = pd.DataFrame({
        "nome": ["  Ana  ", " Bruno"]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_text()

    assert result["nome"].tolist() == ["Ana", "Bruno"]


def test_normalize_text_upper_preserves_accents():
    df = pd.DataFrame({
        "nome": [" João ", "Álvaro"]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_text(colunas="nome", upper=True)

    assert result["nome"].tolist() == ["JOÃO", "ÁLVARO"]


def test_normalize_text_upper_remove_accents():
    df = pd.DataFrame({
        "nome": [" João ", "Álvaro"]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_text(
        colunas="nome",
        upper=True,
        remover_acentos=True
    )

    assert result["nome"].tolist() == ["JOAO", "ALVARO"]


def test_normalize_text_lower_remove_accents():
    df = pd.DataFrame({
        "cidade": [" São Paulo ", "Belo Horizonte"]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_text(
        colunas="cidade",
        lower=True,
        remover_acentos=True
    )

    assert result["cidade"].tolist() == ["sao paulo", "belo horizonte"]


def test_normalize_text_name_titlecase():
    df = pd.DataFrame({
        "nome": ["joão da silva", "MARIA DE SOUZA"]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_text(colunas="nome", name=True)

    assert result["nome"].tolist() == [
        "João da Silva",
        "Maria de Souza"
    ]


def test_normalize_text_create_new_column():
    df = pd.DataFrame({
        "nome": [" João "]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_text(
        colunas="nome",
        upper=True,
        criar_nova_coluna=True
    )

    assert result["nome"].tolist() == [" João "]
    assert result["nome_clean"].tolist() == ["JOÃO"]


def test_normalize_text_multiple_columns():
    df = pd.DataFrame({
        "nome": [" João "],
        "cidade": [" São Paulo "]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_text(
        colunas=["nome", "cidade"],
        lower=True
    )

    assert result["nome"].tolist() == ["joão"]
    assert result["cidade"].tolist() == ["são paulo"]


def test_normalize_text_ignores_invalid_column():
    df = pd.DataFrame({
        "nome": ["Ana"]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_text(
        colunas="coluna_fake",
        upper=True
    )

    assert result.equals(df)

def test_normalize_text_all_string_columns():
    df = pd.DataFrame({
        "nome": [" João "],
        "cidade": [" São Paulo "],
        "idade": [30]
    })

    cleaner = Standard_text(df)
    result = cleaner.normalize_text(lower=True)

    assert result["nome"].tolist() == ["joão"]
    assert result["cidade"].tolist() == ["são paulo"]
    assert result["idade"].tolist() == [30]



def test_drop_exact_duplicates_basic():
    df = pd.DataFrame({
        "nome": ["Ana", "Ana", "Bruno"],
        "idade": [30, 30, 40]
    })

    cleaner = Standard_text(df)
    result = cleaner.drop_exact_duplicates()

    expected = pd.DataFrame({
        "nome": ["Ana", "Bruno"],
        "idade": [30, 40]
    })

    pd.testing.assert_frame_equal(result, expected)


def test_drop_exact_duplicates_partial_not_removed():
    df = pd.DataFrame({
        "nome": ["Ana", "Ana"],
        "idade": [30, 31]  # diferença mínima
    })

    cleaner = Standard_text(df)
    result = cleaner.drop_exact_duplicates()

    assert len(result) == 2


def test_drop_exact_duplicates_resets_index():
    df = pd.DataFrame({
        "nome": ["Ana", "Ana", "Bruno"],
        "idade": [30, 30, 40]
    })

    cleaner = Standard_text(df)
    result = cleaner.drop_exact_duplicates()

    assert list(result.index) == [0, 1]


def test_drop_exact_duplicates_no_duplicates():
    df = pd.DataFrame({
        "nome": ["Ana", "Bruno"],
        "idade": [30, 40]
    })

    cleaner = Standard_text(df)
    result = cleaner.drop_exact_duplicates()

    pd.testing.assert_frame_equal(result, df)


def test_drop_exact_duplicates_empty_df():
    df = pd.DataFrame()

    cleaner = Standard_text(df)
    result = cleaner.drop_exact_duplicates()

    assert result.empty


def test_drop_exact_duplicates_updates_self_df():
    df = pd.DataFrame({
        "x": [1, 1, 2]
    })

    cleaner = Standard_text(df)
    _ = cleaner.drop_exact_duplicates()

    assert len(cleaner.df) == 2




def test_remover_emojis_basic():
    df = pd.DataFrame({
        "nome": ["Rezende🌻", "Ribeiro⚡☄️🌪️"]
    })

    cleaner = Standard_text(df)
    result = cleaner.remover_emojis_e_simbolos()

    assert result["nome"].tolist() == ["Rezende", "Ribeiro"]

def test_remover_emojis_preserve_hyphen_and_numbers():
    df = pd.DataFrame({
        "nome": ["João-Pedro 🚀 123"]
    })

    cleaner = Standard_text(df)
    result = cleaner.remover_emojis_e_simbolos()

    assert result["nome"].tolist() == ["João-Pedro 123"]


def test_remover_emojis_remove_symbols_and_normalize_spaces():
    df = pd.DataFrame({
        "texto": ["Ana ❤️   Silva   ⭐"]
    })

    cleaner = Standard_text(df)
    result = cleaner.remover_emojis_e_simbolos()

    assert result["texto"].tolist() == ["Ana Silva"]


def test_remover_emojis_empty_string_becomes_na():
    df = pd.DataFrame({
        "texto": ["🔥🔥🔥"]
    })

    cleaner = Standard_text(df)
    result = cleaner.remover_emojis_e_simbolos()

    assert pd.isna(result["texto"].iloc[0])


def test_remover_emojis_string_nan_becomes_na():
    df = pd.DataFrame({
        "texto": ["nan"]
    })

    cleaner = Standard_text(df)
    result = cleaner.remover_emojis_e_simbolos()

    assert pd.isna(result["texto"].iloc[0])


def test_remover_emojis_specific_column_only():
    df = pd.DataFrame({
        "nome": ["Ana 🌟"],
        "cidade": ["São Paulo 🚦"]
    })

    cleaner = Standard_text(df)
    result = cleaner.remover_emojis_e_simbolos(columns="nome")

    assert result["nome"].tolist() == ["Ana"]
    assert result["cidade"].tolist() == ["São Paulo 🚦"]


def test_remover_emojis_multiple_columns():
    df = pd.DataFrame({
        "nome": ["Ana 🌟"],
        "cidade": ["São Paulo 🚦"],
        "idade": [30]
    })

    cleaner = Standard_text(df)
    result = cleaner.remover_emojis_e_simbolos(columns=["nome", "cidade"])

    assert result["nome"].tolist() == ["Ana"]
    assert result["cidade"].tolist() == ["São Paulo"]
    assert result["idade"].tolist() == [30]


def test_remover_emojis_invalid_column_ignored():
    df = pd.DataFrame({
        "nome": ["Ana 🌟"]
    })

    cleaner = Standard_text(df)
    result = cleaner.remover_emojis_e_simbolos(columns="coluna_fake")

    pd.testing.assert_frame_equal(result, df)


def test_remover_emojis_updates_self_df():
    df = pd.DataFrame({
        "nome": ["Ana 🌟"]
    })

    cleaner = Standard_text(df)
    cleaner.remover_emojis_e_simbolos()

    assert cleaner.df["nome"].iloc[0] == "Ana"

'''

