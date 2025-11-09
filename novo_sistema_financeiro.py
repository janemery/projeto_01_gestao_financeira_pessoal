import pandas as pd
import numpy as np
import os

# Configurações opcionais
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

def validar_csv(arquivo_csv):
    
    # Verifica se o arquivo existe
    if not os.path.isfile(arquivo_csv):
        print(f"❌ Arquivo '{arquivo_csv}' não encontrado.")
        return None

    # Tenta ler o CSV
    try:
        df = pd.read_csv(arquivo_csv)
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo: {e}")
        return None

    # Verifica se todas as colunas esperadas estão presentes
    colunas_esperadas = ['receita_despesa', 'valor', 'descricao', 'data_transacao', 'categoria']
    colunas_faltando = [col for col in colunas_esperadas if col not in df.columns]
    if colunas_faltando:
        print(f"❌ Colunas faltando no CSV: {colunas_faltando}")
        return None

    if (df['valor'] < 0).any():
        print("❌ A coluna 'valor' contém valores negativos ou zero.")
        return None

    print("✅ CSV validado com sucesso!")
    return df

def calcular_saldo(df):
    
    # Calcula total de receitas
    total_receitas = df[df['receita_despesa'] == 1]['valor'].sum()
    print(total_receitas)

    # Calcula total de despesas
    total_despesas = df[df['receita_despesa'] == 0]['valor'].sum()
    print(total_despesas)

    # Saldo atual
    saldo_atual = total_receitas - total_despesas

    return saldo_atual

def total_por_categoria(df):

    # Filtra apenas despesas (receita_despesa == 0)
    df_despesas = df[df['receita_despesa'] == 0]

    # Agrupa por categoria e soma os valores
    totais = df_despesas.groupby('categoria')['valor'].sum().to_dict()

    return totais

def main():

    # Lê o CSV
    validar_csv('dados_financeiros.csv')

    # Leitura do arquivo CSV
    df = pd.read_csv('dados_financeiros.csv')

    # Visualizar as 5 primeiras linhas
    print(df.head())
    
    
    saldo = calcular_saldo(df)

    if saldo is not None:
        print(f"Saldo atual: R$ {saldo:.2f}")

    totais_categorias = total_por_categoria(df)

    print("Total por categoria:")
    # print(totais_categorias)
    for cat, val in totais_categorias.items():
        print(f"{cat}: R$ {val:.2f}")


if __name__ == "__main__":
    main()
