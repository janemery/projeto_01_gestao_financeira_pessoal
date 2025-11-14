import numpy as np
import pandas as pd


def calcular_receitas(df):
    """
    Calcula o total de receitas no DataFrame.

    O cálculo considera apenas as linhas em que a coluna
    'receita_despesa' é igual a 1. Os valores são somados e
    retornados como número float.

    Args:
        df (pandas.DataFrame): DataFrame contendo as colunas
            'receita_despesa' e 'valor'.

    Returns:
        float: Total de receitas.
    """
    valores = df["valor"].to_numpy()
    tipos = df["receita_despesa"].to_numpy()
    return valores[tipos == 1].sum()
