from src.domain.vocabulario.voc_endereco import *
import re
from typing import List, Any


def _tokens_vocabulario(vocabulario: dict) -> set[str]:
    """
    Extrai todas as variações textuais do vocabulário.
    """
    tokens = set()

    for grupo in vocabulario.values():
        for canonico, variacoes in grupo.items():
            tokens.add(canonico.lower())
            tokens.update(v.lower() for v in variacoes)

    return tokens

def tokenizar_endereco(
    texto: str,
    vocabulario: dict
) -> List[str]:
    """
    Tokeniza endereço separando letra+número APENAS
    quando a parte textual pertence ao vocabulário.
    """

    if not isinstance(texto, str):
        return []

    texto = texto.strip()

    if not texto:
        return []

    vocab_tokens = _tokens_vocabulario(vocabulario)

    # ======================================================
    # 1️⃣ Normalizar separadores comuns
    # ======================================================
    texto = re.sub(r"[,\.\-]", " ", texto)

    # ======================================================
    # 2️⃣ Separação controlada letra+número
    # ======================================================
    def separar_match(match):
        letras = match.group(1)
        numero = match.group(2)

        if letras.lower() in vocab_tokens:
            return f"{letras} {numero}"

        return match.group(0)  # mantém colado

    texto = re.sub(
        r"([A-Za-zÀ-ÿ]+)(\d+)",
        separar_match,
        texto
    )

    texto = re.sub(
        r"(\d+)([A-Za-zÀ-ÿ]+)",
        lambda m: f"{m.group(1)} {m.group(2)}"
        if m.group(2).lower() in vocab_tokens
        else m.group(0),
        texto
    )

    # ======================================================
    # 3️⃣ Manter apenas letras, números e espaços
    # ======================================================
    texto = re.sub(r"[^A-Za-zÀ-ÿ0-9\s]", " ", texto)

    # ======================================================
    # 4️⃣ Normalizar espaços
    # ======================================================
    texto = re.sub(r"\s+", " ", texto).strip()

    # ======================================================
    # 5️⃣ Tokenizar
    # ======================================================
    return texto.split(" ")


def expandir_tokens_por_vocabulario(
        tokens: List[str],
        vocabulario: dict
) -> List[str]:
    """
    Substitui tokens conhecidos por suas formas canônicas,
    preservando ordem e quantidade.
    """

    if not isinstance(tokens, list):
        return []

    tokens_padronizados = []

    for token in tokens:
        token_upper = token.upper()
        substituido = False

        for forma_canonica, conjunto_tokens in vocabulario.items():
            if token_upper in conjunto_tokens:
                tokens_padronizados.append(forma_canonica)
                substituido = True
                break

        if not substituido:
            tokens_padronizados.append(token)

    return tokens_padronizados


def reordenar_voc_dado_simples(tokens: List[Any]) -> List[Any]:
    """
    Reordena tokens simples no formato [voc, dado] quando o tamanho <= 2.
    """

    if not isinstance(tokens, list):
        return tokens

    if len(tokens) > 2:
        return tokens

    if len(tokens) != 2:
        return tokens

    a, b = tokens

    def eh_dado(x):
        return isinstance(x, (int, float)) or (
                isinstance(x, str) and x.isdigit()
        )

    def eh_voc(x):
        return isinstance(x, str) and not eh_dado(x)

    # Caso: [voc, dado]
    if eh_voc(a) and eh_dado(b):
        return [a, b]

    # Caso: [dado, voc] → reordena
    if eh_dado(a) and eh_voc(b):
        return [b, a]

    return tokens

def reconstruir_texto(tokens: List[Any]) -> str:
    """
    Reconstrói uma string legível a partir de uma lista de tokens.
    """

    if not isinstance(tokens, list):
        return ""

    # converte tudo para string
    partes = [str(token) for token in tokens if token is not None]

    # junta com espaço
    texto = " ".join(partes)

    # normaliza espaços duplicados
    texto = " ".join(texto.split())

    return texto

def normalizar_endereco_texto(texto: str) -> str:
    """
    Orquestra o pipeline de normalização de endereço.
    """

    if not isinstance(texto, str):
        return ""

    tokens = tokenizar_endereco(texto, VOCABULARIO_ENDERECO)
    tokens = expandir_tokens_por_vocabulario(tokens, VOCABULARIO_ENDERECO)
    tokens = reordenar_voc_dado_simples(tokens)

    return reconstruir_texto(tokens)