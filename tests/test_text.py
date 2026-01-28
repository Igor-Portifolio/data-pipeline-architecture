# from src.domain.regras.lingua_regras import *
# from src.pipelines.auto.text_pipeline import *
#
# def test_classificar_string_simples_non_string():
#     assert classificar_string_simples(123) == []
#     assert classificar_string_simples(None) == []
#     assert classificar_string_simples(["abc"]) == []
#
#
# def test_classificar_string_simples_empty_string():
#     assert classificar_string_simples("") == []
#     assert classificar_string_simples("   ") == []
#
#
# def test_classificar_string_simples_short_name():
#     valor = "ana"
#     assert classificar_string_simples(valor) == []
#
#
# def test_classificar_string_simples_exact_length_boundary():
#     # 10 caracteres NÃO ativa NOME_LONGO
#     valor = "abcdefghij"
#     assert classificar_string_simples(valor) == []
#
#
# def test_classificar_string_simples_long_name():
#     valor = "abcdefghijk"  # 11 caracteres
#     resultado = classificar_string_simples(valor)
#
#     assert "NOME_LONGO" in resultado
#     assert len(resultado) == 1
#
#
# def test_classificar_string_simples_email_domain_only():
#     valor = "usuario@gmail.com"
#     resultado = classificar_string_simples(valor)
#
#     assert resultado == ["NOME_LONGO", "DOMINIO_EMAIL"]
#
#
# def test_classificar_string_simples_long_name_and_email():
#     valor = "usuario.muito.longo@gmail.com"
#     resultado = classificar_string_simples(valor)
#
#     assert "NOME_LONGO" in resultado
#     assert "DOMINIO_EMAIL" in resultado
#     assert len(resultado) == 2
#
#
# def test_classificar_string_simples_case_and_whitespace_insensitive():
#     valor = "  Usuario@GMAIL.Com  "
#     resultado = classificar_string_simples(valor)
#
#     assert resultado == ["NOME_LONGO", "DOMINIO_EMAIL"]
#
#
# def test_remover_titulos_non_string():
#     assert remover_titulos_e_profissoes(None) == ""
#     assert remover_titulos_e_profissoes(123) == ""
#     assert remover_titulos_e_profissoes(["dr joao"]) == ""
#
#
# def test_remover_titulos_simple_title():
#     texto = "Dr João Silva"
#     resultado = remover_titulos_e_profissoes(texto)
#
#     assert resultado == "João Silva"
#
#
# def test_remover_titulos_with_dot():
#     texto = "Dra Maria Souza"
#     resultado = remover_titulos_e_profissoes(texto)
#
#     assert resultado == "Maria Souza"
#
#
# def test_remover_titulos_case_insensitive():
#     texto = "dOuToR Carlos Alberto"
#     resultado = remover_titulos_e_profissoes(texto)
#
#     assert resultado == "Carlos Alberto"
#
#
# def test_remover_multiple_titles():
#     texto = "Dr Eng João Pereira"
#     resultado = remover_titulos_e_profissoes(texto)
#
#     assert resultado == "João Pereira"
#
#
# def test_remover_profissao_only():
#     texto = "Advogado Marcos"
#     resultado = remover_titulos_e_profissoes(texto)
#
#     assert resultado == "Marcos"
#
#
# def test_remover_title_in_middle_of_text():
#     texto = "João Silva Engenheiro Civil"
#     resultado = remover_titulos_e_profissoes(texto)
#
#     assert resultado == "João Silva  Civil"
#
#
# def test_remover_title_does_not_remove_partial_words():
#     texto = "Administrador de sistemas"
#     resultado = remover_titulos_e_profissoes(texto)
#
#     assert resultado == "de sistemas"
#
#
# def test_remover_unknown_words_unchanged():
#     texto = "Coordenador João"
#     resultado = remover_titulos_e_profissoes(texto)
#
#     assert resultado == "Coordenador João"
#
#
# def test_remover_trailing_and_leading_spaces():
#     texto = "  Sr João da Silva  "
#     resultado = remover_titulos_e_profissoes(texto)
#
#     assert resultado == "João da Silva"
#
#
# def test_normalizar_caracteres_nome_non_string():
#     assert normalizar_caracteres_nome(None) == ""
#     assert normalizar_caracteres_nome(123) == ""
#     assert normalizar_caracteres_nome(["João"]) == ""
#
#
# def test_normalizar_caracteres_nome_simple():
#     texto = "João Silva"
#     assert normalizar_caracteres_nome(texto) == "João Silva"
#
#
# def test_normalizar_caracteres_nome_removes_numbers_and_symbols():
#     texto = "João123 @Silva!"
#     esperado = "João Silva"
#     assert normalizar_caracteres_nome(texto) == esperado
#
#
# def test_normalizar_caracteres_nome_keeps_accents():
#     texto = "Álvaro Núñez"
#     assert normalizar_caracteres_nome(texto) == "Álvaro Núñez"
#
#
# def test_normalizar_caracteres_nome_keeps_apostrophe_in_middle():
#     texto = "d'Ávila"
#     assert normalizar_caracteres_nome(texto) == "d'Ávila"
#
#
# def test_normalizar_caracteres_nome_removes_apostrophe_at_edges():
#     texto = "'João'"
#     assert normalizar_caracteres_nome(texto) == "João"
#
#
# def test_normalizar_caracteres_nome_removes_isolated_apostrophe_between_spaces():
#     texto = "João ' Silva"
#     assert normalizar_caracteres_nome(texto) == "João Silva"
#
#
# def test_normalizar_caracteres_nome_normalizes_spaces():
#     texto = "  João    da   Silva  "
#     esperado = "João da Silva"
#     assert normalizar_caracteres_nome(texto) == esperado
#
#
# def test_normalizar_caracteres_nome_only_invalid_characters():
#     texto = "1234 !!!"
#     assert normalizar_caracteres_nome(texto) == ""
#
#
# def test_eh_nome_linguisticamente_invalido_non_string():
#     assert eh_nome_linguisticamente_invalido(None) is True
#     assert eh_nome_linguisticamente_invalido(123) is True
#     assert eh_nome_linguisticamente_invalido(["João"]) is True
#
#
# def test_eh_nome_linguisticamente_invalido_valid_name():
#     assert eh_nome_linguisticamente_invalido("João Silva") is False
#     assert eh_nome_linguisticamente_invalido("Maria de Souza") is False
#
#
# def test_eh_nome_linguisticamente_invalido_family_terms():
#     assert eh_nome_linguisticamente_invalido("mae") is True
#     assert eh_nome_linguisticamente_invalido("Meu pai") is True
#     assert eh_nome_linguisticamente_invalido("irmã") is True
#     assert eh_nome_linguisticamente_invalido("tio Carlos") is True
#
#
# def test_eh_nome_linguisticamente_invalido_religious_entities():
#     assert eh_nome_linguisticamente_invalido("Deus") is True
#     assert eh_nome_linguisticamente_invalido("Jesus Cristo") is True
#     assert eh_nome_linguisticamente_invalido("Espírito Santo") is True
#
#
# def test_eh_nome_linguisticamente_invalido_religious_phrases():
#     assert eh_nome_linguisticamente_invalido("Deus é fiel") is True
#     assert eh_nome_linguisticamente_invalido("abençoado por Deus") is True
#     assert eh_nome_linguisticamente_invalido("Graças a Deus") is True
#
#
# def test_eh_nome_linguisticamente_invalido_invalid_answers():
#     assert eh_nome_linguisticamente_invalido("não sei") is True
#     assert eh_nome_linguisticamente_invalido("Nao Informado") is True
#     assert eh_nome_linguisticamente_invalido("prefiro nao dizer") is True
#     assert eh_nome_linguisticamente_invalido("Anônimo") is True
#
#
# def test_eh_nome_linguisticamente_invalido_invalid_tokens():
#     assert eh_nome_linguisticamente_invalido("nome") is True
#     assert eh_nome_linguisticamente_invalido("teste") is True
#     assert eh_nome_linguisticamente_invalido("xxxx") is True
#     assert eh_nome_linguisticamente_invalido("abc") is True
#
#
# def test_eh_nome_linguisticamente_invalido_case_insensitive():
#     assert eh_nome_linguisticamente_invalido("DEUS") is True
#     assert eh_nome_linguisticamente_invalido("MaE") is True
#     assert eh_nome_linguisticamente_invalido("NaO SeI") is True
#
#
# def test_eh_nome_linguisticamente_invalido_word_boundary():
#     # Não deve marcar substrings parciais
#     assert eh_nome_linguisticamente_invalido("maestro") is False
#     assert eh_nome_linguisticamente_invalido("paises") is False
#     assert eh_nome_linguisticamente_invalido("nomeado") is False
#
#
# def test_eh_nome_linguisticamente_invalido_phrase_inside_text():
#     assert eh_nome_linguisticamente_invalido("João deus é fiel") is True
#     assert eh_nome_linguisticamente_invalido("Maria graças a Deus") is True
#
# def test_pipeline_limpar_nome_domain_non_string():
#     assert pipeline_limpar_nome_domain(None) is pd.NA
#     assert pipeline_limpar_nome_domain(123) is pd.NA
#     assert pipeline_limpar_nome_domain(["João"]) is pd.NA
#
#
# def test_pipeline_limpar_nome_domain_simple_valid_name():
#     texto = "João Silva"
#     resultado = pipeline_limpar_nome_domain(texto)
#
#     assert resultado == "João Silva"
#
#
# def test_pipeline_limpar_nome_domain_removes_titles():
#     texto = "Dr João Silva"
#     resultado = pipeline_limpar_nome_domain(texto)
#
#     assert resultado == "João Silva"
#
#
# def test_pipeline_limpar_nome_domain_removes_profession_and_normalizes():
#     texto = "Eng. João123 da Silva!!!"
#     resultado = pipeline_limpar_nome_domain(texto)
#
#     assert resultado == "João da Silva"
#
#
# def test_pipeline_limpar_nome_domain_invalid_linguistic_term():
#     texto = "Deus é fiel"
#     resultado = pipeline_limpar_nome_domain(texto)
#
#     assert resultado is pd.NA
#
#
# def test_pipeline_limpar_nome_domain_invalid_answer():
#     texto = "não informado"
#     resultado = pipeline_limpar_nome_domain(texto)
#
#     assert resultado is pd.NA
#
#
# def test_pipeline_limpar_nome_domain_only_numbers_and_symbols():
#     texto = "12345 !!!"
#     resultado = pipeline_limpar_nome_domain(texto)
#
#     assert resultado is pd.NA
#
#
# def test_pipeline_limpar_nome_domain_family_term():
#     texto = "mae"
#     resultado = pipeline_limpar_nome_domain(texto)
#
#     assert resultado is pd.NA
#
#
# def test_pipeline_limpar_nome_domain_trims_and_cleans():
#     texto = "   Sr  João   d'Ávila!!   "
#     resultado = pipeline_limpar_nome_domain(texto)
#
#     assert resultado == "João d'Ávila"
#
#
# def test_pipeline_limpar_nome_domain_edge_valid_after_cleaning():
#     texto = "Adv Maria"
#     resultado = pipeline_limpar_nome_domain(texto)
#
#     assert resultado == "Maria"
#
# def test_text_basic_pipelines_default_behavior():
#     df = pd.DataFrame({
#         "nome": ["João 😊", "Árvore-azul"],
#         "cidade": ["São Paulo 🌆", "Belo-Horizonte"]
#     })
#
#     resultado = text_basic_pipelines(df)
#
#     assert resultado["nome"].tolist() == ["JOAO", "ARVORE-AZUL"]
#     assert resultado["cidade"].tolist() == ["SAO PAULO", "BELO-HORIZONTE"]
