#
# def test_pipeline_bairro_domain_retorna_string_vazia_para_none():
#     assert pipeline_bairro_domain(None) == ""
#
# 
# def test_pipeline_bairro_domain_retorna_string_vazia_para_tipo_invalido():
#     assert pipeline_bairro_domain(123) == ""
#     assert pipeline_bairro_domain([]) == ""
#     assert pipeline_bairro_domain({}) == ""
#
#
# def test_pipeline_bairro_domain_expande_jardim():
#     texto = "jd paulista"
#     esperado = "JARDIM PAULISTA"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_expande_vila():
#     texto = "vl maria"
#     esperado = "VILA MARIA"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_expande_parque():
#     texto = "pq das rosas"
#     esperado = "PARQUE DAS ROSAS"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_expande_com_pontuacao():
#     texto = "jd europa"
#     esperado = "JARDIM EUROPA"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_expande_multiplos_tokens():
#     texto = "jd res hab"
#     esperado = "JARDIM RESIDENCIAL HABITACIONAL"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_expande_santa():
#     texto = "vl sta maria"
#     esperado = "VILA SANTA MARIA"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_expande_santo():
#     texto = "pq sto antonio"
#     esperado = "PARQUE SANTO ANTONIO"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_expande_industrial():
#     texto = "pq ind"
#     esperado = "PARQUE INDUSTRIAL"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_nao_altera_tokens_desconhecidos():
#     texto = "bairro aleatorio xpto"
#     esperado = "BAIRRO ALEATORIO XPTO"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_normaliza_para_uppercase():
#     texto = "Vl Maria"
#     esperado = "VILA MARIA"
#
#     assert pipeline_bairro_domain(texto) == esperado
#
#
# def test_pipeline_bairro_domain_e_idempotente_para_texto_normalizado():
#     texto = "JARDIM PAULISTA"
#
#     assert pipeline_bairro_domain(texto) == texto
#
#
# def test_pipeline_bairro_domain_idempotencia_com_frase_complexa():
#     texto = "PARQUE RESIDENCIAL SANTO ANTONIO"
#
#     assert pipeline_bairro_domain(texto) == texto
#
