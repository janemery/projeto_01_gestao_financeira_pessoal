import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from financeiro.despesas import calcular_despesas
from financeiro.receitas import calcular_receitas

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


def calcular_saldo(df):
    """
    Calcula o saldo total no DataFrame.

    O saldo corresponde à soma das receitas menos a soma
    das despesas, considerando os valores na coluna 'valor'
    filtrados pela coluna 'receita_despesa'.

    Args:
        df (pandas.DataFrame): DataFrame contendo as colunas
            'valor' e 'receita_despesa'.

    Returns:
        float: Valor numérico do saldo calculado.
    """
    valores = df["valor"].to_numpy()
    tipos = df["receita_despesa"].to_numpy()
    return valores[tipos == 1].sum() - valores[tipos == 0].sum()


def total_por_categoria(df):
    """
    Calcula o total de despesas agrupadas por categoria.

    Apenas registros classificados como despesa
    ('receita_despesa' == 0) são considerados.

    Args:
        df (pandas.DataFrame): DataFrame contendo as colunas
            'categoria', 'valor' e 'receita_despesa'.

    Returns:
        dict: Mapeamento categoria → total de despesas.
    """
    df_despesas = df[df["receita_despesa"] == 0]
    return df_despesas.groupby("categoria")["valor"].sum().to_dict()


def total_categorias_por_periodo(df, data_inicio, data_fim):
    """
    Calcula o total de valores por categoria dentro de um período.

    As datas são convertidas para datetime e o DataFrame é
    filtrado pelo intervalo fornecido. Apenas categorias presentes
    no período filtrado são incluídas no resultado.

    Args:
        df (pandas.DataFrame): DataFrame contendo 'data_transacao',
            'categoria', 'valor' e 'receita_despesa'.
        data_inicio (str): Data inicial no formato dd/mm/aaaa.
        data_fim (str): Data final no formato dd/mm/aaaa.

    Returns:
        dict or None: Totais por categoria ou None se as datas
            forem inválidas.
    """

    def parse_data(data_str):
        """
        Converte uma string de data para datetime.

        Args:
            data_str (str): Data no formato dd/mm/aaaa ou dd/mm/aa.

        Returns:
            pandas.Timestamp or None: Objeto de data ou None se inválida.
        """
        formatos = ("%d/%m/%Y", "%d/%m/%y")
        for fmt in formatos:
            try:
                return pd.to_datetime(data_str, format=fmt)
            except (ValueError, TypeError):
                continue
        logger.error("Data inválida: %s", data_str)
        return None

    inicio = parse_data(data_inicio)
    fim = parse_data(data_fim)

    if not inicio or not fim:
        logger.error("Datas inválidas. Operação cancelada.")
        return None

    df["data_transacao"] = pd.to_datetime(
        df["data_transacao"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    filtro = (df["data_transacao"] >= inicio) & (
        df["data_transacao"] <= fim
    )
    df_filtrado = df[filtro]

    if df_filtrado.empty:
        logger.info("Nenhuma transação encontrada no período informado.")
        return {}

    return df_filtrado.groupby("categoria")["valor"].sum().to_dict()


def exibir_extrato(df):
    """
    Exibe o extrato de transações ordenado por data.

    O extrato inclui data, tipo (receita ou despesa),
    descrição, categoria e valor.

    Args:
        df (pandas.DataFrame): DataFrame contendo as colunas
            'data_transacao', 'receita_despesa',
            'descricao', 'categoria' e 'valor'.

    Returns:
        None
    """
    logger.info("Exibindo extrato.")

    if df["data_transacao"].dtype == "object":
        df["data_transacao"] = pd.to_datetime(
            df["data_transacao"],
            format="%d/%m/%Y",
            errors="coerce"
        )

    df = df.sort_values(by="data_transacao")

    print("\nExtrato de Transações")
    print(
        f"Período: {df['data_transacao'].min().strftime('%d/%m/%Y')} "
        f"até {df['data_transacao'].max().strftime('%d/%m/%Y')}\n"
    )

    for _, row in df.iterrows():
        tipo = "Receita" if row["receita_despesa"] == 1 else "Despesa"
        data = row["data_transacao"].strftime("%d/%m/%Y")
        print(
            f"{data} | {tipo:<8} | {row['descricao']:<25} | "
            f"{row['categoria']:<15} | R$ {row['valor']:>8.2f}"
        )

    total_receitas = df[df["receita_despesa"] == 1]["valor"].sum()
    total_despesas = df[df["receita_despesa"] == 0]["valor"].sum()
    saldo = total_receitas - total_despesas

    print("\nTotais:")
    print(f"Total de Receitas: R$ {total_receitas:,.2f}")
    print(f"Total de Despesas: R$ {total_despesas:,.2f}")
    print(f"Saldo Atual: R$ {saldo:,.2f}")


def resumo_financeiro(df):
    """
    Exibe um resumo financeiro com totais globais e por categoria.

    O resumo apresenta:
      - total de receitas,
      - total de despesas,
      - totais de despesas agrupados por categoria.

    Args:
        df (pandas.DataFrame): DataFrame contendo transações.

    Returns:
        None
    """
    logger.info("Exibindo resumo financeiro.")
    totais_categoria = total_por_categoria(df)
    total_receitas = calcular_receitas(df)
    total_despesas = calcular_despesas(df)

    print("\nResumo Financeiro:")
    print(f"Total de receitas: R$ {total_receitas:,.2f}")
    print("Total por categoria:")
    for cat, val in totais_categoria.items():
        print(f"  - {cat:<15}: R$ {val:,.2f}")
    print("-----------------------------")
    print(f"Total de despesas: R$ {total_despesas:,.2f}")


def gerar_relatorio_categorias(df, nome_arquivo="relatorio_categorias.png"):
    """
    Gera um gráfico de totais por categoria e salva em arquivo.

    O gráfico é exibido e salvo na pasta 'relatorios'. Caso a
    pasta não exista, ela será criada automaticamente.

    Args:
        df (pandas.DataFrame): DataFrame já agregado por categoria.
        nome_arquivo (str): Nome do arquivo PNG de destino.

    Returns:
        None
    """
    if not os.path.exists("relatorios"):
        os.makedirs("relatorios")

    plt.figure(figsize=(8, 5))
    df.plot(kind="bar")
    plt.title("Receitas e Despesas por Categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Valor (R$)")
    plt.tight_layout()

    caminho = os.path.join("relatorios", nome_arquivo)
    plt.savefig(caminho)
    plt.show()

    logger.info("Relatório salvo em '%s'", caminho)


def exibir_total_categorias_periodo(df):
    """
    Solicita um período ao usuário e exibe os totais por categoria.

    A função coleta datas via input, obtém os totais e imprime
    o resultado formatado. Em caso de erro, mensagens são exibidas
    no console e registradas no log.

    Args:
        df (pandas.DataFrame): DataFrame com transações financeiras.

    Returns:
        None
    """
    data_inicio = input("Informe a data inicial (dd/mm/aaaa): ")
    data_fim = input("Informe a data final (dd/mm/aaaa): ")

    totais_periodo = total_categorias_por_periodo(
        df, data_inicio, data_fim
    )

    if not totais_periodo:
        logger.error("Não foi possível calcular os totais.")
    else:
        print("\nTotais por Categoria no Período:")
        print(f"Período: {data_inicio} - {data_fim}\n")
        for categoria, valor in totais_periodo.items():
            print(f"  - {categoria:<15}: R$ {valor:,.2f}")
