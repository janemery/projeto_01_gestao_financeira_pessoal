import pandas as pd
import numpy as np

# Configurações opcionais
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

# Leitura do arquivo CSV
df = pd.read_csv('dados_financeiros.csv')

# Visualizar as 5 primeiras linhas
print(df.head())

def calcular_saldo(arquivo_csv):
    """
    Lê um arquivo CSV contendo registros financeiros e calcula o saldo atual.
    O CSV deve ter as colunas: tipo (receita/despesa) e valor.
    """
    # Lê o CSV
    try:
        df = pd.read_csv(arquivo_csv)
    except FileNotFoundError:
        print(f"❌ Arquivo '{arquivo_csv}' não encontrado.")
        return None

    # Verifica se as colunas necessárias existem
    if 'receita_despesa' not in df.columns or 'valor' not in df.columns:
        print("❌ O CSV precisa conter as colunas 'receita_despesa' e 'valor'.")
        return None

    # Calcula total de receitas
    total_receitas = df[df['receita_despesa'] == 1]['valor'].sum()
    print(total_receitas)

    # Calcula total de despesas
    total_despesas = df[df['receita_despesa'] == 0]['valor'].sum()
    print(total_despesas)

    # Saldo atual
    saldo_atual = total_receitas - total_despesas

    return saldo_atual

arquivo = 'dados_financeiros.csv'
saldo = calcular_saldo(arquivo)
if saldo is not None:
    print(f"Saldo atual: R$ {saldo:.2f}")

def total_por_categoria(arquivo_csv):
    """
    Calcula o total de valores por categoria para despesas.
    
    Parâmetros:
    - arquivo_csv: caminho para o CSV com as colunas ['receita_despesa', 'valor', 'categoria']
    
    Retorna:
    - dicionário com categoria como chave e total como valor
    """
    # Lê o CSV
    try:
        df = pd.read_csv(arquivo_csv)
    except FileNotFoundError:
        print(f"❌ Arquivo '{arquivo_csv}' não encontrado.")
        return None

    # Verifica se as colunas necessárias existem
    for col in ['receita_despesa', 'valor', 'categoria']:
        if col not in df.columns:
            print(f"❌ O CSV precisa conter a coluna '{col}'.")
            return None

    # Filtra apenas despesas (receita_despesa == 0)
    df_despesas = df[df['receita_despesa'] == 0]

    # Agrupa por categoria e soma os valores
    totais = df_despesas.groupby('categoria')['valor'].sum().to_dict()

    return totais

arquivo = 'dados_financeiros.csv'
totais_categorias = total_por_categoria(arquivo)

print("Total por categoria:")
for cat, val in totais_categorias.items():
    print(f"{cat}: R$ {val:.2f}")
