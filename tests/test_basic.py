# import pandas as pd
# from datetime import datetime
# from src.core.basic_regras import *
# from src.pipelines.auto.basic_pipeline import *
#
# def test_coerce_value_nulls():
#     assert coerce_value(None) is pd.NA
#     assert coerce_value(pd.NA) is pd.NA
#     assert coerce_value("") is pd.NA
#     assert coerce_value("   ") is pd.NA
#
#
# def test_coerce_value_numeric_passthrough():
#     assert coerce_value(10) == 10
#     assert coerce_value(10.5) == 10.5
#
#
# def test_coerce_value_dates():
#     assert coerce_value("05/01/2024") == datetime(2024, 1, 5)
#     assert coerce_value("2024-01-05") == datetime(2024, 1, 5)
#     assert coerce_value("20240105") == datetime(2024, 1, 5)
#
#
# def test_coerce_value_brazilian_currency():
#     assert coerce_value("R$ 1.234,50") == 1234.50
#     assert coerce_value("1.234,50") == 1234.50
#
#
# def test_coerce_value_international_currency():
#     assert coerce_value("1,234.50") == 1234.50
#     assert coerce_value("12,345.67") == 12345.67
#
#
# def test_coerce_value_integer_string():
#     assert coerce_value("23") == 23
#     assert coerce_value(" 045 ") == 45
#
#
# def test_coerce_value_simple_float():
#     assert coerce_value("10.5") == 10.5
#     assert coerce_value("  3.14 ") == 3.14
#
#
# def test_coerce_value_fallback_string():
#     assert coerce_value("ABC123") == "ABC123"
#     assert coerce_value("Rua das Flores") == "Rua das Flores"
#
#
# def test_coerce_value_other_types():
#     assert coerce_value(["a", "b"]) == ["a", "b"]
#     assert coerce_value({"a": 1}) == {"a": 1}
#
#
# def test_trim_whitespace_na():
#     assert pd.isna(trim_whitespace_value(pd.NA))
#     assert trim_whitespace_value(None) is None
#
#
# def test_trim_whitespace_simple_string():
#     assert trim_whitespace_value(" abc ") == "abc"
#
#
# def test_trim_whitespace_multiple_spaces():
#     assert trim_whitespace_value("a   b    c") == "a b c"
#
#
# def test_trim_whitespace_invisible_space():
#     texto = "a\u00A0\u00A0b"
#     assert trim_whitespace_value(texto) == "a b"
#
#
# def test_trim_whitespace_only_spaces():
#     assert trim_whitespace_value("   ") == ""
#
#
# def test_trim_whitespace_list_basic():
#     entrada = [" a ", " b ", "c"]
#     esperado = ["a", "b", "c"]
#
#     assert trim_whitespace_value(entrada) == esperado
#
#
# def test_trim_whitespace_list_preserves_empty_strings():
#     entrada = [" a ", "   ", "", " b "]
#     esperado = ["a", "", "", "b"]
#
#     assert trim_whitespace_value(entrada) == esperado
#
#
# def test_trim_whitespace_list_mixed_types():
#     entrada = [" a ", 10, None, " b "]
#     esperado = ["a", 10, None, "b"]
#
#     assert trim_whitespace_value(entrada) == esperado
#
#
# def test_trim_whitespace_other_types():
#     assert trim_whitespace_value(10) == 10
#     assert trim_whitespace_value({"a": 1}) == {"a": 1}
#
#
# def test_normalizar_pontuacao_texto_non_string():
#     assert normalizar_pontuacao_texto(123) is None
#     assert normalizar_pontuacao_texto(None) is None
#     assert normalizar_pontuacao_texto(["abc"]) is None
#
#
# def test_normalizar_pontuacao_texto_empty_string():
#     assert normalizar_pontuacao_texto("") is None
#     assert normalizar_pontuacao_texto("   ") is None
#
#
# def test_normalizar_pontuacao_texto_simple_text():
#     assert normalizar_pontuacao_texto("Olá mundo") == "Olá mundo"
#
#
# def test_normalizar_pontuacao_texto_removes_punctuation():
#     texto = "Olá, mundo! Tudo bem?"
#     esperado = "Olá mundo Tudo bem"
#     assert normalizar_pontuacao_texto(texto) == esperado
#
#
# def test_normalizar_pontuacao_texto_keeps_accents():
#     texto = "ação, coração; órgão!"
#     esperado = "ação coração órgão"
#     assert normalizar_pontuacao_texto(texto) == esperado
#
#
# def test_normalizar_pontuacao_texto_removes_underscores():
#     texto = "nome_completo_do_cliente"
#     esperado = "nome completo do cliente"
#     assert normalizar_pontuacao_texto(texto) == esperado
#
#
# def test_normalizar_pontuacao_texto_apostrophe_in_middle_kept():
#     texto = "d'água l'amour rock'n'roll"
#     esperado = "d'água l'amour rock'n'roll"
#     assert normalizar_pontuacao_texto(texto) == esperado
#
#
# def test_normalizar_pontuacao_texto_multiple_spaces_normalized():
#     texto = "Olá     mundo   bonito"
#     esperado = "Olá mundo bonito"
#     assert normalizar_pontuacao_texto(texto) == esperado
#
#
# def test_normalizar_pontuacao_texto_only_punctuation():
#     texto = "!!! ??? ---"
#     assert normalizar_pontuacao_texto(texto) is None
#
#
# def test_normalizar_pontuacao_texto_mixed_case():
#     texto = "  João_d'Ávila!!!  "
#     esperado = "João d'Ávila"
#     assert normalizar_pontuacao_texto(texto) == esperado
#
#
# def test_ordenar_coluna_alfa_basic():
#     df = pd.DataFrame(
#         {
#             "nome": ["Carlos", "ana", "Bruno"]
#         }
#     )
#
#     resultado = ordenar_coluna_alfa(df, "nome")
#
#     assert resultado == ["ana", "Bruno", "Carlos"]
#
#
# def test_ordenar_coluna_alfa_ignores_case():
#     df = pd.DataFrame(
#         {
#             "nome": ["zebra", "Abelha", "cachorro"]
#         }
#     )
#
#     resultado = ordenar_coluna_alfa(df, "nome")
#
#     assert resultado == ["Abelha", "cachorro", "zebra"]
#
#
# def test_ordenar_coluna_alfa_ignores_whitespace():
#     df = pd.DataFrame(
#         {
#             "nome": ["  Bruno", "ana  ", " Carlos "]
#         }
#     )
#
#     resultado = ordenar_coluna_alfa(df, "nome")
#
#     assert resultado == ["ana  ", "  Bruno", " Carlos "]
#
#
# def test_ordenar_coluna_alfa_converts_to_string():
#     df = pd.DataFrame(
#         {
#             "codigo": [10, 2, 1]
#         }
#     )
#
#     resultado = ordenar_coluna_alfa(df, "codigo")
#
#     assert resultado == ["1", "10", "2"]
#
#
# def test_ordenar_coluna_alfa_with_none_values():
#     df = pd.DataFrame(
#         {
#             "nome": ["Carlos", None, "Ana"]
#         }
#     )
#
#     resultado = ordenar_coluna_alfa(df, "nome")
#
#     assert resultado == ["Ana", "Carlos", "None"]
#
#
# def test_ordenar_coluna_alfa_empty_dataframe():
#     df = pd.DataFrame({"nome": []})
#
#     resultado = ordenar_coluna_alfa(df, "nome")
#
#     assert resultado == []
#
#
# def test_ordenar_coluna_alfa_column_not_found():
#     df = pd.DataFrame(
#         {
#             "nome": ["Ana", "Bruno"]
#         }
#     )
#
#     try:
#         ordenar_coluna_alfa(df, "idade")
#         assert False, "Esperado KeyError"
#     except KeyError as e:
#         assert "idade" in str(e)
#
#
# def test_valores_unicos_basic():
#     entrada = ["a", "b", "a", "c", "b"]
#     esperado = ["a", "b", "c"]
#
#     assert valores_unicos(entrada) == esperado
#
#
# def test_valores_unicos_preserves_order():
#     entrada = ["x", "y", "x", "x", "z", "y"]
#     esperado = ["x", "y", "z"]
#
#     assert valores_unicos(entrada) == esperado
#
#
# def test_valores_unicos_single_element():
#     entrada = ["a"]
#     esperado = ["a"]
#
#     assert valores_unicos(entrada) == esperado
#
#
# def test_valores_unicos_empty_list():
#     assert valores_unicos([]) == []
#
#
# def test_valores_unicos_all_duplicates():
#     entrada = ["a", "a", "a"]
#     esperado = ["a"]
#
#     assert valores_unicos(entrada) == esperado
#
#
# def test_valores_unicos_non_list_input():
#     assert valores_unicos("abc") == []
#     assert valores_unicos(None) == []
#     assert valores_unicos(123) == []
#
#
# def test_valores_unicos_mixed_values():
#     entrada = ["a", "A", "a", "b", "B"]
#     esperado = ["a", "A", "b", "B"]
#
#     assert valores_unicos(entrada) == esperado
#
# def test_basic_pipeline_applies_all_steps_in_correct_order():
#     df = pd.DataFrame(
#         {
#             "coluna": [
#                 "  10 ",
#                 "  João!!! ",
#                 "  abc  ",
#                 None
#             ]
#         }
#     )
#
#     resultado = basic_pipeline(df)
#
#     esperado = pd.DataFrame(
#         {
#             "coluna": [
#                 10,          # trim -> coerce
#                 "João",      # trim -> coerce (string) -> normaliza pontuação
#                 "abc",       # trim -> coerce (string) -> normaliza
#                 None         # preservado
#             ]
#         }
#     )
#
#     pd.testing.assert_frame_equal(resultado, esperado)
#
