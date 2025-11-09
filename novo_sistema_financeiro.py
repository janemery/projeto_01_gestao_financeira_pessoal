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

def total_categorias_por_periodo(df, data_inicio, data_fim):
    # Converte a coluna de datas para datetime
    df['data_transacao'] = pd.to_datetime(df['data_transacao'], format='%d/%m/%Y', errors='coerce')

    # Converte datas de input para datetime
    inicio = pd.to_datetime(data_inicio, format='%d/%m/%Y')
    fim = pd.to_datetime(data_fim, format='%d/%m/%Y')

    # Filtra apenas despesas dentro do período
    filtro = (df['receita_despesa'] == 0) & (df['data_transacao'] >= inicio) & (df['data_transacao'] <= fim)
    df_filtrado = df[filtro]

    # Agrupa por categoria e soma os valores
    totais = df_filtrado.groupby('categoria')['valor'].sum()

    # Converte para dicionário e retorna
    return totais.to_dict()

def exibir_extrato(df):
    
    # # Verifica se o DataFrame está vazio
    # if df.empty:
    #     print("⚠️ Nenhuma transação encontrada.")
    #     return

    # Converte a coluna de data, se necessário
    if df['data_transacao'].dtype == 'object':
        df['data_transacao'] = pd.to_datetime(df['data_transacao'], format='%d/%m/%Y', errors='coerce')

    # Ordena por data
    df = df.sort_values(by='data_transacao')

    print("\n=== 💰 EXTRATO DE TRANSAÇÕES ===")
    print(f"Período: {df['data_transacao'].min().strftime('%d/%m/%Y')} até {df['data_transacao'].max().strftime('%d/%m/%Y')}\n")

    for _, row in df.iterrows():
        tipo = "Receita" if row['receita_despesa'] == 1 else "Despesa"
        data = row['data_transacao'].strftime("%d/%m/%Y")
        print(f"{data} | {tipo:<8} | {row['descricao']:<25} | {row['categoria']:<15} | R$ {row['valor']:>8.2f}")

    # Mostra totais
    total_receitas = df[df['receita_despesa'] == 1]['valor'].sum()
    total_despesas = df[df['receita_despesa'] == 0]['valor'].sum()
    saldo = total_receitas - total_despesas

    print("\n--- Totais ---")
    print(f"📈 Total de Receitas: R$ {total_receitas:,.2f}")
    print(f"📉 Total de Despesas: R$ {total_despesas:,.2f}")
    print(f"💵 Saldo Atual: R$ {saldo:,.2f}")

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

    print(totais_categorias)
    for cat, val in totais_categorias.items():
        print(f"{cat}: R$ {val:.2f}")
    
    # Exemplo de uso:
    resultado = total_categorias_por_periodo(df, '01/04/2025', '28/04/2025')
    print(f"total_categorias_por_periodo {resultado}")

    exibir_extrato(df)


if __name__ == "__main__":
    main()
