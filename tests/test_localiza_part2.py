import pytest
from typing import List
from src.domain.rules.address import *

#
# def test_tem_mesmo_prefixo_prefixos_iguais_retorna_true():
#     assert tem_mesmo_prefixo("Santana", "Santo Amaro", n=3) is True
#
#
# def test_tem_mesmo_prefixo_prefixos_diferentes_retorna_false():
#     assert tem_mesmo_prefixo("Centro", "Santana", n=3) is False
#
#
# def test_tem_mesmo_prefixo_respeita_parametro_n():
#     assert tem_mesmo_prefixo("ABCdef", "ABCxyz", n=3) is True
#     assert tem_mesmo_prefixo("ABCdef", "ABXxyz", n=3) is False
#     assert tem_mesmo_prefixo("ABCdef", "ABXxyz", n=2) is True
#
#
# def test_tem_mesmo_prefixo_strings_identicas_retorna_true():
#     assert tem_mesmo_prefixo("Industrial", "Industrial", n=3) is True
#     assert tem_mesmo_prefixo("Industrial", "Industrial", n=5) is True
#
#
# def test_tem_mesmo_prefixo_strings_menores_que_n():
#     assert tem_mesmo_prefixo("AB", "AB", n=3) is True
#     assert tem_mesmo_prefixo("AB", "AC", n=3) is False
#
#
# def test_tem_mesmo_prefixo_strings_vazias():
#     assert tem_mesmo_prefixo("", "", n=3) is True
#
#
# def test_tem_mesmo_prefixo_case_sensitive():
#     assert tem_mesmo_prefixo("abc", "Abc", n=3) is False
#
#
# def test_tem_mesmo_prefixo_nao_modifica_entradas():
#     a = "Santana"
#     b = "Santo Amaro"
#
#     _ = tem_mesmo_prefixo(a, b, n=3)
#
#     assert a == "Santana"
#     assert b == "Santo Amaro"
#
#












# ---------- helpers fake ----------

def always_false(*args, **kwargs) -> bool:
    return False


def always_true(*args, **kwargs) -> bool:
    return True


def prefix_only(a: str, b: str, n: int) -> bool:
    return a[:n] == b[:n]


# ---------- testes ----------

def test_lista_vazia_dispara_erro():
    with pytest.raises(ValueError):
        group_similar_bairros([])


def test_lista_com_apenas_espacos_retorna_vazio():
    result = group_similar_bairros(["  ", "", None])
    assert result == []


def test_sem_similaridade_gera_grupos_unitarios(monkeypatch):
    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.tem_mesmo_prefixo",
        always_false
    )
    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.eh_similar_jaro_winkler",
        always_false
    )

    bairros = ["Centro", "Jardim", "Industrial"]
    result = group_similar_bairros(bairros)

    assert result == [["Centro"], ["Jardim"], ["Industrial"]]


def test_similaridade_por_prefixo(monkeypatch):
    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.tem_mesmo_prefixo",
        prefix_only
    )
    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.eh_similar_jaro_winkler",
        always_false
    )

    bairros = ["Santana", "Santo Amaro", "Centro"]
    result = group_similar_bairros(bairros, prefix_length=3)

    assert result == [["Santana", "Santo Amaro"], ["Centro"]]


def test_similaridade_por_jaro(monkeypatch):
    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.tem_mesmo_prefixo",
        always_false
    )
    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.eh_similar_jaro_winkler",
        always_true
    )

    bairros = ["Vila Maria", "Vila Mária", "Centro"]
    result = group_similar_bairros(bairros)

    assert result == [["Vila Maria", "Vila Mária", "Centro"]]


def test_quebra_de_grupo_funciona(monkeypatch):
    calls = []

    def fake_jaro(a, b, fator):
        calls.append((a, b))
        return a.startswith("Vila") and b.startswith("Vila")

    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.tem_mesmo_prefixo",
        always_false
    )
    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.eh_similar_jaro_winkler",
        fake_jaro
    )

    bairros = ["Vila Nova", "Vila Velha", "Centro", "Central"]
    result = group_similar_bairros(bairros)

    assert result == [["Vila Nova", "Vila Velha"], ["Centro"], ["Central"]]
    assert len(calls) > 0  # garante que a função foi usada


def test_ordem_e_preservada(monkeypatch):
    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.tem_mesmo_prefixo",
        always_true
    )
    monkeypatch.setattr(
        "src.domain.rules.endereco_regras.eh_similar_jaro_winkler",
        always_false
    )

    bairros = ["B", "A", "C"]
    result = group_similar_bairros(bairros)

    assert result == [["B", "A", "C"]]
