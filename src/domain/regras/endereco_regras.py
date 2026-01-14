from src.domain.vocabulario.voc_endereco import *
import re
from typing import List, Any
import jellyfish
from typing import List, Optional



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


def tokenizar_bairro(texto: str, vocab: dict) -> List[str]:
    """
    Tokenização tolerante:
    separa tokens colados APENAS quando começam
    com abreviação conhecida no vocabulário.
    """

    if not isinstance(texto, str):
        return []

    texto = texto.strip().upper()

    if not texto:
        return []

    # --------------------------------------------------
    # 1️⃣ Extrair todos os prefixos válidos do vocabulário
    # --------------------------------------------------
    prefixos_validos = set()

    for _, variacoes in vocab.items():
        for v in variacoes:
            prefixos_validos.add(v.upper())

    # ordena do maior para o menor (STA antes de ST)
    prefixos_validos = sorted(prefixos_validos, key=len, reverse=True)

    # --------------------------------------------------
    # 2️⃣ Tokenização base
    # --------------------------------------------------
    tokens = re.split(r"\s+", texto)
    resultado = []

    # --------------------------------------------------
    # 3️⃣ Separação tolerante controlada
    # --------------------------------------------------
    for token in tokens:
        separado = False

        for prefixo in prefixos_validos:
            if token.startswith(prefixo) and token != prefixo:
                resto = token[len(prefixo):]

                # só separa se o resto tiver letras
                if resto.isalpha():
                    resultado.append(prefixo)
                    resultado.append(resto)
                    separado = True
                    break

        if not separado:
            resultado.append(token)

    return resultado


def expandir_tokens_bairro(tokens: List[str], vocab: dict) -> List[str]:
    """
    Expande tokens usando vocabulário explícito.
    Ex: STA -> SANTA
    """

    if not isinstance(tokens, list):
        return []

    resultado = []

    for token in tokens:
        token_upper = token.upper()
        expandido = token  # default: mantém

        for forma_canonica, variacoes in vocab.items():
            if token_upper in {v.upper() for v in variacoes}:
                expandido = forma_canonica
                break

        resultado.append(expandido)

    return resultado


def reconstruir_texto_bairro(tokens: List[str]) -> str:
    """
    Reconstrói o texto do bairro a partir de tokens.
    """

    if not isinstance(tokens, list):
        return ""

    partes = [
        str(token).strip()
        for token in tokens
        if isinstance(token, str) and token.strip()
    ]

    texto = " ".join(partes)

    # segurança: normaliza espaços duplicados
    return " ".join(texto.split())


def normalizar_bairro_texto(texto: str) -> str:
    """
    Orquestra o pipeline de normalização de bairro.
    """

    if not isinstance(texto, str):
        return ""

    tokens = tokenizar_bairro(texto, VOCABULARIO_BAIRRO)
    tokens = expandir_tokens_bairro(tokens, VOCABULARIO_BAIRRO)

    return reconstruir_texto_bairro(tokens)


def extrair_prefixo(texto: str, n: int = 3) -> str:
    """
    Extrai os primeiros n caracteres de uma string.
    Se a string tiver menos que n caracteres, retorna tudo.
    """

    if not isinstance(texto, str) or not texto:
        return ""

    texto = texto.strip()
    return texto[:n]  # pode ajustar para upper() se preferir


def tem_mesmo_prefixo(texto1: str, texto2: str, n: int = 3) -> bool:
    """
    Verifica se duas strings possuem o mesmo prefixo de tamanho n.
    """
    prefixo1 = extrair_prefixo(texto1, n)
    prefixo2 = extrair_prefixo(texto2, n)

    return prefixo1 == prefixo2


def score_jaro_winkler(a: str, b: str) -> float:
    """
    Calcula o score de similaridade Jaro-Winkler entre duas strings.

    Retorno:
    float entre 0.0 e 1.0
    """

    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0

    a = a.strip()
    b = b.strip()

    if not a or not b:
        return 0.0

    return jellyfish.jaro_winkler_similarity(a, b)


def eh_similar_jaro_winkler(
        a: str,
        b: str,
        fator: float
) -> bool:
    """
    Decide se duas strings são similares com base
    no score de Jaro-Winkler e um fator mínimo.
    """

    if not isinstance(fator, (int, float)):
        raise ValueError(f"Fator inválido: {fator}")

    score = score_jaro_winkler(a, b)

    return score >= fator


def group_similar_bairros(
        bairros: List[str],
        prefix_length: int = 3,
        jaro_threshold: float = 0.88  # valor comum para nomes de lugares no Brasil
) -> List[List[str]]:
    if not bairros:
        raise ValueError("A lista de bairros não pode estar vazia.")

    # Remove espaços extras e normaliza (opcional, mas recomendado)
    bairros = [b.strip() for b in bairros if b and b.strip()]

    if not bairros:
        return []

    groups: List[List[str]] = []
    current_group: List[str] = [bairros[0]]

    for i in range(1, len(bairros)):
        prev = current_group[-1]
        curr = bairros[i]

        # Critério de união: prefixo igual OU similaridade alta
        sao_similares = (
                tem_mesmo_prefixo(prev, curr, n=prefix_length) or
                eh_similar_jaro_winkler(prev, curr, fator=jaro_threshold)
        )

        if sao_similares:
            current_group.append(curr)
        else:
            groups.append(current_group)
            current_group = [curr]

    # Não esquecer o último grupo
    if current_group:
        groups.append(current_group)

    return groups


def escolher_melhor_match(
    grupos: List[List[str]],
    candidatos: List[str],
    limiar_alto: float = 0.9
) -> List[Optional[str]]:
    """
    Para cada grupo de variações, escolhe o melhor candidato possível
    baseado em Jaro-Winkler.

    Regras:
    - Se grupo tem tamanho 1 → retorna esse valor
    - Match exato → para imediatamente
    - Score >= limiar_alto → para imediatamente
    - Mantém ordem dos grupos
    """

    resultados: List[Optional[str]] = []

    for grupo in grupos:

        # --------------------------------------------------
        # Caso trivial
        # --------------------------------------------------
        if not grupo:
            resultados.append(None)
            continue

        if len(grupo) == 1:
            resultados.append(grupo[0])
            continue

        melhor_score = -1.0
        melhor_match = None

        # --------------------------------------------------
        # Cruzamento variações × candidatos
        # --------------------------------------------------
        for variante in grupo:
            v_norm = variante.strip()

            for candidato in candidatos:
                c_norm = candidato.strip()

                # Match exato → prioridade máxima
                if v_norm == c_norm:
                    melhor_match = candidato
                    melhor_score = 1.0
                    break

                score = score_jaro_winkler(v_norm, c_norm)

                if score > melhor_score:
                    melhor_score = score
                    melhor_match = candidato

                # Match forte → para busca
                if score >= limiar_alto:
                    break

            if melhor_score == 1.0 or melhor_score >= limiar_alto:
                break

        resultados.append(melhor_match)

    return resultados

