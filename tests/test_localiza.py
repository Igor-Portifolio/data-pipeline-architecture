from src.domain.regras.endereco_regras import *
#
#
# def test_texto_nao_string():
#     assert tokenizar_endereco(None, VOCABULARIO_ENDERECO) == []
#     assert tokenizar_endereco(123, VOCABULARIO_ENDERECO) == []
#     assert tokenizar_endereco([], VOCABULARIO_ENDERECO) == []
#
#
# def test_texto_vazio():
#     assert tokenizar_endereco("", VOCABULARIO_ENDERECO) == []
#     assert tokenizar_endereco("   ", VOCABULARIO_ENDERECO) == []
#
#
# def test_normaliza_separadores():
#     texto = "Rua.ABC-123,Centro"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["Rua", "ABC", "123", "Centro"]
#
#
# def test_separa_letra_numero_quando_vocabulario():
#     texto = "Rua123"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["Rua", "123"]
#
#
# def test_separa_numero_letra_quando_vocabulario():
#     texto = "123Rua"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["123", "Rua"]
#
#
# def test_nao_separa_letra_numero_fora_vocabulario():
#     texto = "ABC123"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["ABC123"]
#
#
# def test_nao_separa_numero_letra_fora_vocabulario():
#     texto = "123ABC"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["123ABC"]
#
#
# def test_endereco_completo_realista():
#     texto = "Av Paulista, 123 Ap45 BlB"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["Av", "Paulista", "123", "Ap", "45", "BlB"]
#
#
# def test_remove_caracteres_invalidos():
#     texto = "Rua@ ABC#123!"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["Rua", "ABC", "123"]
#
#
# def test_normaliza_espacos():
#     texto = "Rua     ABC     123"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["Rua", "ABC", "123"]
#
#
# def test_preserva_acentos():
#     texto = "Praça Sé 100"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["Praça", "Sé", "100"]
#
#
# def test_excecao_sem_numero():
#     texto = "Rua ABC s/n"
#     resultado = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
#     assert resultado == ["Rua", "ABC", "s", "n"]
#
#
# def test_expandir_tokens_logradouro_simples():
#     tokens = ["rua", "av", "travessa"]
#     esperado = ["RUA", "AVENIDA", "TRAVESSA"]
#
#     resultado = expandir_tokens_por_vocabulario(tokens, VOCABULARIO_ENDERECO)
#
#     assert resultado == esperado
#
#
# def test_expandir_tokens_preserva_desconhecidos():
#     tokens = ["rua", "xyz", "casa"]
#     esperado = ["RUA", "xyz", "CASA"]
#
#     resultado = expandir_tokens_por_vocabulario(tokens, VOCABULARIO_ENDERECO)
#
#     assert resultado == esperado
#
#
# def test_expandir_tokens_preserva_ordem_e_quantidade():
#     tokens = ["av", "av", "rua"]
#     esperado = ["AVENIDA", "AVENIDA", "RUA"]
#
#     resultado = expandir_tokens_por_vocabulario(tokens, VOCABULARIO_ENDERECO)
#
#     assert resultado == esperado
#
#
# def test_expandir_tokens_unidades_prediais():
#     tokens = ["ap", "bloco", "casa"]
#     esperado = ["APARTAMENTO", "BLOCO", "CASA"]
#
#     resultado = expandir_tokens_por_vocabulario(tokens, VOCABULARIO_ENDERECO)
#
#     assert resultado == esperado
#
#
# def test_expandir_tokens_complementos():
#     tokens = ["fundos", "frt", "esquina"]
#     esperado = ["FUNDOS", "FRENTE", "ESQUINA"]
#
#     resultado = expandir_tokens_por_vocabulario(tokens, VOCABULARIO_ENDERECO)
#
#     assert resultado == esperado
#
#
# def test_expandir_tokens_excecoes():
#     tokens = ["s/n", "nao informado", "abc"]
#     esperado = ["SEM_NUMERO", "NAO_INFORMADO", "abc"]
#
#     resultado = expandir_tokens_por_vocabulario(tokens, VOCABULARIO_ENDERECO)
#
#     assert resultado == esperado
#
#
# def test_expandir_tokens_token_ja_canonico():
#     tokens = ["RUA", "AVENIDA"]
#     esperado = ["RUA", "AVENIDA"]
#
#     resultado = expandir_tokens_por_vocabulario(tokens, VOCABULARIO_ENDERECO)
#
#     assert resultado == esperado
#
#
# def test_expandir_tokens_input_invalido():
#     assert expandir_tokens_por_vocabulario(None, VOCABULARIO_ENDERECO) == []
#     assert expandir_tokens_por_vocabulario("rua", VOCABULARIO_ENDERECO) == []
#
#
# def test_reordenar_voc_dado_simples_input_nao_lista():
#     assert reordenar_voc_dado_simples(None) is None
#     assert reordenar_voc_dado_simples("rua 123") == "rua 123"
#
#
# def test_reordenar_voc_dado_simples_lista_vazia():
#     assert reordenar_voc_dado_simples([]) == []
#
#
# def test_reordenar_voc_dado_simples_um_elemento():
#     assert reordenar_voc_dado_simples(["rua"]) == ["rua"]
#     assert reordenar_voc_dado_simples([123]) == [123]
#
#
# def test_reordenar_voc_dado_simples_tamanho_maior_que_dois():
#     tokens = ["rua", 123, "ap"]
#     assert reordenar_voc_dado_simples(tokens) == tokens
#
#
# def test_reordenar_voc_dado_simples_voc_dado_ordem_correta():
#     tokens = ["rua", 123]
#     assert reordenar_voc_dado_simples(tokens) == ["rua", 123]
#
#
# def test_reordenar_voc_dado_simples_dado_voc_reordena():
#     tokens = [123, "rua"]
#     assert reordenar_voc_dado_simples(tokens) == ["rua", 123]
#
#
# def test_reordenar_voc_dado_simples_dado_string_numerica():
#     tokens = ["123", "rua"]
#     assert reordenar_voc_dado_simples(tokens) == ["rua", "123"]
#
#
# def test_reordenar_voc_dado_simples_float_como_dado():
#     tokens = [12.5, "apto"]
#     assert reordenar_voc_dado_simples(tokens) == ["apto", 12.5]
#
#
# def test_reordenar_voc_dado_simples_dois_vocs():
#     tokens = ["rua", "apto"]
#     assert reordenar_voc_dado_simples(tokens) == tokens
#
#
# def test_reordenar_voc_dado_simples_dois_dados():
#     tokens = [123, "456"]
#     assert reordenar_voc_dado_simples(tokens) == tokens
#
#
# def test_reordenar_voc_dado_simples_ordem_preservada_quando_indefinido():
#     tokens = ["123", "456"]
#     assert reordenar_voc_dado_simples(tokens) == tokens
#
#
# def test_reconstruir_texto_lista_simples():
#     tokens = ["Rua", "das", "Flores", "123"]
#     assert reconstruir_texto(tokens) == "Rua das Flores 123"
#
#
# def test_reconstruir_texto_remove_none():
#     tokens = ["Avenida", None, "Brasil"]
#     assert reconstruir_texto(tokens) == "Avenida Brasil"
#
#
# def test_reconstruir_texto_converte_para_string():
#     tokens = ["Número", 10, 2.5]
#     assert reconstruir_texto(tokens) == "Número 10 2.5"
#
#
# def test_reconstruir_texto_normaliza_espacos():
#     tokens = ["Rua", " ", "das", "", "Flores"]
#     assert reconstruir_texto(tokens) == "Rua das Flores"
#
#
# def test_reconstruir_texto_lista_vazia():
#     assert reconstruir_texto([]) == ""
#
#
# def test_reconstruir_texto_nao_lista():
#     assert reconstruir_texto("Rua 123") == ""
#
#
# def test_reconstruir_texto_lista_com_espacos_extras():
#     tokens = ["  Rua", "das   ", " Flores "]
#     assert reconstruir_texto(tokens) == "Rua das Flores"
#
#
# def test_pipeline_endereco_domain_input_nao_string():
#     assert pipeline_endereco_domain(None) == ""
#     assert pipeline_endereco_domain(123) == ""
#     assert pipeline_endereco_domain(["rua", "123"]) == ""
#
#
# def test_pipeline_endereco_domain_string_vazia():
#     assert pipeline_endereco_domain("") == ""
#
#
# def test_pipeline_endereco_domain_rua_com_numero_ordem_correta():
#     resultado = pipeline_endereco_domain("rua 123")
#     assert resultado == "RUA 123"
#
#
# def test_pipeline_endereco_domain_numero_rua_reordena():
#     resultado = pipeline_endereco_domain("123 rua")
#     assert resultado == "RUA 123"
#
#
# def test_pipeline_endereco_domain_abreviacao_expandida():
#     resultado = pipeline_endereco_domain("av paulista")
#     assert resultado == "AVENIDA PAULISTA"
#
#
# def test_pipeline_endereco_domain_apartamento_expandido():
#     resultado = pipeline_endereco_domain("rua a ap 45")
#     assert resultado == "RUA A APARTAMENTO 45"
#
#
#
# def test_pipeline_endereco_domain_complemento():
#     resultado = pipeline_endereco_domain("av brasil fundos")
#     assert resultado == "AVENIDA BRASIL FUNDOS"
#
#
# def test_pipeline_endereco_domain_texto_sem_vocabulario():
#     resultado = pipeline_endereco_domain("bairro centro")
#     assert resultado == "BAIRRO CENTRO"
#
#
# def test_pipeline_endereco_domain_apenas_numero():
#     resultado = pipeline_endereco_domain("123")
#     assert resultado == "123"
#
#
# def test_pipeline_endereco_domain_ordem_preservada_quando_nao_simples():
#     resultado = pipeline_endereco_domain("rua das flores 123 ap 45")
#     assert resultado == "RUA DAS FLORES 123 APARTAMENTO 45"
#
#
# def test_tokenizar_bairro_tipo_invalido():
#     assert tokenizar_bairro(123, VOCABULARIO_BAIRRO) == []
#     assert tokenizar_bairro(None, VOCABULARIO_BAIRRO) == []
#
#
# def test_tokenizar_bairro_string_vazia():
#     assert tokenizar_bairro("", VOCABULARIO_BAIRRO) == []
#     assert tokenizar_bairro("   ", VOCABULARIO_BAIRRO) == []
#
#
# def test_tokenizar_bairro_simples_sem_prefixo():
#     texto = "CENTRO"
#     esperado = ["CENTRO"]
#
#     assert tokenizar_bairro(texto, VOCABULARIO_BAIRRO) == esperado
#
#
# def test_tokenizar_bairro_prefixo_colado_separa():
#     texto = "JDPAULISTA"
#     esperado = ["JD", "PAULISTA"]
#
#     assert tokenizar_bairro(texto, VOCABULARIO_BAIRRO) == esperado
#
#
# def test_tokenizar_bairro_prefixo_colado_com_espaco():
#     texto = "JD PAULISTA"
#     esperado = ["JD", "PAULISTA"]
#
#     assert tokenizar_bairro(texto, VOCABULARIO_BAIRRO) == esperado
#
#
# def test_tokenizar_bairro_nao_separa_se_resto_nao_for_letra():
#     texto = "JD123"
#     esperado = ["JD123"]
#
#     assert tokenizar_bairro(texto, VOCABULARIO_BAIRRO) == esperado
#
#
# def test_tokenizar_bairro_prefixo_exato_nao_separa():
#     texto = "JD"
#     esperado = ["JD"]
#
#     assert tokenizar_bairro(texto, VOCABULARIO_BAIRRO) == esperado
#
#
# def test_tokenizar_bairro_prioriza_prefixo_maior():
#     texto = "STAPAULO"
#     esperado = ["STA", "PAULO"]
#
#     assert tokenizar_bairro(texto, VOCABULARIO_BAIRRO) == esperado
#
#
# def test_tokenizar_bairro_multiplos_tokens():
#     texto = "JDPAULISTA VL NOVA"
#     esperado = ["JD", "PAULISTA", "VL", "NOVA"]
#
#     assert tokenizar_bairro(texto, VOCABULARIO_BAIRRO) == esperado
#
#
# def test_tokenizar_bairro_mantem_tokens_desconhecidos():
#     texto = "BAIRRO X"
#     esperado = ["BAIRRO", "X"]
#
#     assert tokenizar_bairro(texto, VOCABULARIO_BAIRRO) == esperado
#
#
# def test_tokenizar_bairro_normaliza_para_maiusculas():
#     texto = "jdPaulista"
#     esperado = ["JD", "PAULISTA"]
#
#     assert tokenizar_bairro(texto, VOCABULARIO_BAIRRO) == esperado
#

def test_pipeline_bairro_domain_retorna_string_vazia_para_none():
    assert pipeline_bairro_domain(None) == ""


def test_pipeline_bairro_domain_retorna_string_vazia_para_tipo_invalido():
    assert pipeline_bairro_domain(123) == ""
    assert pipeline_bairro_domain([]) == ""
    assert pipeline_bairro_domain({}) == ""


def test_pipeline_bairro_domain_expande_jardim():
    texto = "jd paulista"
    esperado = "JARDIM PAULISTA"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_expande_vila():
    texto = "vl maria"
    esperado = "VILA MARIA"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_expande_parque():
    texto = "pq das rosas"
    esperado = "PARQUE DAS ROSAS"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_expande_com_pontuacao():
    texto = "jd europa"
    esperado = "JARDIM EUROPA"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_expande_multiplos_tokens():
    texto = "jd res hab"
    esperado = "JARDIM RESIDENCIAL HABITACIONAL"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_expande_santa():
    texto = "vl sta maria"
    esperado = "VILA SANTA MARIA"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_expande_santo():
    texto = "pq sto antonio"
    esperado = "PARQUE SANTO ANTONIO"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_expande_industrial():
    texto = "pq ind"
    esperado = "PARQUE INDUSTRIAL"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_nao_altera_tokens_desconhecidos():
    texto = "bairro aleatorio xpto"
    esperado = "BAIRRO ALEATORIO XPTO"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_normaliza_para_uppercase():
    texto = "Vl Maria"
    esperado = "VILA MARIA"

    assert pipeline_bairro_domain(texto) == esperado


def test_pipeline_bairro_domain_e_idempotente_para_texto_normalizado():
    texto = "JARDIM PAULISTA"

    assert pipeline_bairro_domain(texto) == texto


def test_pipeline_bairro_domain_idempotencia_com_frase_complexa():
    texto = "PARQUE RESIDENCIAL SANTO ANTONIO"

    assert pipeline_bairro_domain(texto) == texto

