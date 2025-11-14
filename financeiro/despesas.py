import numpy as np
import pandas as pd


def calcular_despesas(df):
    """
    Calcula o total de despesas no DataFrame.

    Apenas linhas em que 'receita_despesa' é igual a 0 são
    consideradas. A função soma os valores dessas linhas e
    retorna o total.

    Args:
        df (pandas.DataFrame): DataFrame contendo as colunas
            'receita_despesa' e 'valor'.

    Returns:
        float: Soma dos valores classificados como despesa.
    """
    valores = df["valor"].to_numpy()
    tipos = df["receita_despesa"].to_numpy()
    return valores[tipos == 0].sum()
