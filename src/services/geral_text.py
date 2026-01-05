import pandas as pd
import re
from typing import List, Optional, Union
from unidecode import unidecode
from pathlib import Path
from src.domain.vocabulario import *
from src.domain.lingua_regras import *


class Standard_text:

    def __init__(self, df: pd.DataFrame, ):
        self.df = df.copy()

    def _remover_acentos(self, texto: str) -> str:
        if not isinstance(texto, str):
            return texto
        return unidecode(texto)

    def _titlecase_inteligente(self, texto: str) -> str:
        if pd.isna(texto) or str(texto).strip() == '' or str(texto) == 'nan':
            return texto

        texto = str(texto).strip()
        palavras = texto.split()
        resultado = []

        for i, palavra in enumerate(palavras):
            if not palavra:
                continue
            palavra_lower = palavra.lower()

            # Preposição e não é a primeira palavra → minúscula
            if palavra_lower in self.preposicoes_minusculas and i != 0:
                resultado.append(palavra_lower)
            else:
                resultado.append(palavra.capitalize())

        return ' '.join(resultado)

    def create_feedback_file(rev: str) -> Path:
        """
        Cria a pasta 'text_files' ao lado da pasta src.
        Gera um arquivo client_feedback_<rev>.txt.
        Se já existir, sobrescreve.
        """

        # Caminho absoluto deste arquivo
        current_file = Path(__file__).resolve()

        # Raiz do projeto (pasta pai da src)
        project_root = current_file.parent.parent

        # Pasta de saída
        folder = project_root / "text_files"
        folder.mkdir(exist_ok=True)

        # Nome baseado na revisão
        file_name = f"client_feedback_{rev}.txt"
        file_path = folder / file_name

        # Cria ou sobrescreve
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{rev}:\n\n")

        return file_path

    def normalize_nulls(
            self,
            coluna: str = None,
            nulo: str = None
    ) -> pd.DataFrame:
        """
        Trata valores nulos no DataFrame.

        - coluna=None  → aplica a todas as colunas
        - nulo=None    → converte nulos para NaN
        - nulo="texto" → substitui nulos pela string fornecida
        """

        df = self.df.copy()

        def substituir(serie: pd.Series):
            if nulo is None:
                # deixa em NaN
                return serie.replace(["", " ", "nan", "None"], pd.NA)
            else:
                # substitui nulos pela string
                return serie.replace(["", " ", "nan", "None", pd.NA], nulo)

        # Se nenhuma coluna foi especificada → todas
        if coluna is None:
            for col in df.columns:
                df[col] = substituir(df[col])
        else:
            if coluna not in df.columns:
                raise KeyError(f"Coluna '{coluna}' não encontrada no DataFrame!")

            df[coluna] = substituir(df[coluna])

        # Atualiza self.df e retorna
        self.df = df
        return df

    def _get_string_columns(self) -> list:
        return list(self.df.select_dtypes(include=["object", "string"]).columns)

    def normalize_text(
            self,
            colunas: Optional[Union[str, List[str]]] = None,
            upper: bool = False,
            lower: bool = False,
            name: bool = False,  # Title Case Brasileiro
            remover_acentos: bool = False,
            criar_nova_coluna: bool = False,
    ) -> pd.DataFrame:
        """
        Normaliza texto com opções brasileiras profissionais
        Pode ser aplicado em uma ou várias colunas de uma aez
        """
        if colunas is None:
            cols_para_tratar = self.df.select_dtypes(include=["object", "string"]).columns
        else:
            cols_para_tratar = [colunas] if isinstance(colunas, str) else colunas

        for col in cols_para_tratar:
            if col not in self.df.columns:
                continue
            serie = self.df[col].astype(str).str.strip()

            if upper:
                nova_serie = serie.str.upper()
            elif lower:
                nova_serie = serie.str.lower()
            elif name:
                nova_serie = serie.apply(self._titlecase_inteligente)
            else:
                nova_serie = serie  # só trim

            if remover_acentos:
                nova_serie = nova_serie.apply(self._remover_acentos)

            if criar_nova_coluna:
                novo_nome = f"{col}_clean"
                self.df[novo_nome] = nova_serie
            else:
                self.df[col] = nova_serie

        return self.df

    def drop_exact_duplicates(self) -> pd.DataFrame:

        antes = len(self.df)
        self.df = self.df.drop_duplicates(ignore_index=True).copy()
        removidas = antes - len(self.df)
        return self.df

    def remover_emojis_e_simbolos(self, columns=None) -> pd.DataFrame:
        """
        Remove emojis, símbolos, caracteres especiais e pictogramas
        das colunas de texto. Mantém apenas letras, números, espaços e hífen.
        """

        df = self.df.copy()

        # Define colunas alvo
        if columns is None:
            text_cols = df.select_dtypes(
                include=['object', 'string', 'category']
            ).columns
        else:
            if isinstance(columns, str):
                columns = [columns]
            text_cols = columns

        # Regex de emojis e pictogramas
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U0001F900-\U0001F9FF"
            "\U00002600-\U000026FF"
            "\U00002700-\U000027BF"
            "\U000024C2-\U0001F251"
            "\U0001F004\U0001F0CF\U0001F18E\U0001F191-\U0001F19A"
            "\U0001F201-\U0001F251"
            "]+",
            flags=re.UNICODE
        )

        # Remove qualquer coisa que não seja letra, número, espaço ou hífen
        limpeza_final = re.compile(r'[^\w\s\-]')

        for col in text_cols:
            if col not in df.columns:
                continue

            serie = df[col].astype(str)

            serie = serie.str.replace(emoji_pattern, '', regex=True)
            serie = serie.str.replace(limpeza_final, ' ', regex=True)
            serie = serie.str.strip()
            serie = serie.str.replace(r'\s+', ' ', regex=True)

            serie = serie.replace(['', 'nan'], pd.NA)

            df[col] = serie

        self.df = df
        return df


    def limpar_nomes_proprios(
            self,
            coluna: str
    ) -> pd.DataFrame:
        """
        Aplica a limpeza de nomes próprios a uma coluna do DataFrame.
        """

        if coluna not in self.df.columns:
            raise KeyError(f"Coluna '{coluna}' não encontrada.")

        self.df[coluna] = (
            self.df[coluna]
            .apply(limpar_nome_unitario)
        )

        return self.df

    def coletar_casos_suspeitos(
            self,
            df: pd.DataFrame,
            coluna_nome: str,
    ) -> pd.DataFrame:
        """
        Coleta registros suspeitos e aplica revisão automática
        removendo domínios de e-mail conhecidos, mesmo sem '@'.
        """

        if coluna_nome not in df.columns:
            raise KeyError(f"Coluna '{coluna_nome}' não encontrada no DataFrame.")

        registros = []

        for idx, valor in df[coluna_nome].items():
            if not isinstance(valor, str):
                continue

            motivos = classificar_string_simples(valor)

            if not motivos:
                continue

            valor_revisado = valor

            # ======================================================
            # REGRA — remover domínio de e-mail conhecido
            # ======================================================
            if "DOMINIO_EMAIL" in motivos:
                valor_lower = valor.lower()

                for dominio in DOMINIOS_EMAIL_COMUNS:
                    dominio_lower = dominio.lower()

                    # variações possíveis
                    variantes = {
                        dominio_lower,
                        dominio_lower.replace(".", ""),
                    }

                    for variante in variantes:
                        pos = valor_lower.find(variante)
                        if pos != -1:
                            valor_revisado = valor[:pos]
                            break

                    if valor_revisado != valor:
                        break

            valor_revisado = valor_revisado.strip()

            registros.append({
                "id_registro": idx,
                "valor_original": valor,
                "motivos": motivos,
                "regras_aplicadas": motivos.copy(),
                "valor_revisado": valor_revisado,
            })

        return pd.DataFrame(
            registros,
            columns=[
                "id_registro",
                "valor_original",
                "motivos",
                "regras_aplicadas",
                "valor_revisado",
            ],
        )


