import logging
import os

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

pd.set_option("display.max_rows", 10)
pd.set_option("display.float_format", lambda x: f"{x:.2f}")


def validar_csv(arquivo_csv):
    """
    Valida um arquivo CSV contendo dados financeiros.

    O arquivo é verificado quanto à existência, leitura correta,
    presença das colunas obrigatórias e integridade dos valores.
    Retorna um DataFrame válido ou None caso haja algum problema.

    Args:
        arquivo_csv (str): Caminho para o arquivo CSV.

    Returns:
        pandas.DataFrame or None: O DataFrame validado ou None se a validação falhar.
    """
    if not os.path.isfile(arquivo_csv):
        logger.error("Arquivo '%s' não encontrado.", arquivo_csv)
        return None

    try:
        df = pd.read_csv(arquivo_csv)
    except Exception as exc:
        logger.error("Erro ao ler o arquivo: %s", exc)
        return None

    colunas_esperadas = [
        "receita_despesa",
        "valor",
        "descricao",
        "data_transacao",
        "categoria",
    ]

    colunas_faltando = [
        col for col in colunas_esperadas if col not in df.columns
    ]
    if colunas_faltando:
        logger.error("Colunas faltando no CSV: %s", colunas_faltando)
        return None

    if (df["valor"] < 0).any():
        logger.error("A coluna 'valor' contém valores inválidos.")
        return None

    return df
