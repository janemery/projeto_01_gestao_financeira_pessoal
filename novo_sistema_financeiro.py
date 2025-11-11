import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

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

    # print("✅ CSV validado com sucesso!")
    return df

def calcular_despesas(df):
    # Converte colunas para arrays NumPy
    valores = df['valor'].to_numpy()
    tipos = df['receita_despesa'].to_numpy()

    # Seleciona apenas despesas (receita_despesa == 0) e soma
    total_despesas = valores[tipos == 0].sum()
    return total_despesas

def calcular_receitas(df):
    # Converte colunas para arrays NumPy
    valores = df['valor'].to_numpy()
    tipos = df['receita_despesa'].to_numpy()

    # Seleciona apenas receitas (receita_despesa == 1) e soma
    total_receitas = valores[tipos == 1].sum()
    return total_receitas

def calcular_saldo(df):
    # Converte colunas para arrays NumPy
    valores = df['valor'].to_numpy()
    tipos = df['receita_despesa'].to_numpy()  # 1 = receita, 0 = despesa

    # Calcula saldo usando indexação booleana
    saldo_atual = valores[tipos == 1].sum() - valores[tipos == 0].sum()

    return saldo_atual

def total_por_categoria(df):

    # Filtra apenas despesas (receita_despesa == 0)
    df_despesas = df[df['receita_despesa'] == 0]

    # Agrupa por categoria e soma os valores
    totais = df_despesas.groupby('categoria')['valor'].sum().to_dict()

    return totais

def total_categorias_por_periodo(df, data_inicio, data_fim):

    def parse_data(data_str):
    # Tenta converter datas nos formatos dd/mm/aaaa e dd/mm/aa.
    # Retorna um objeto datetime, ou None se a data for inválida.
    
        for fmt in ("%d/%m/%Y", "%d/%m/%y"):
            try:
                return pd.to_datetime(data_str, format=fmt)
            except (ValueError, TypeError):
                continue

        # Se chegou aqui, nenhuma conversão funcionou
        print(f"⚠️  Erro: a data '{data_str}' é inválida.")
        print("   → Use o formato DD/MM/AAAA (ex: 30/11/2025) e verifique se a data existe.")
        return None

    # 🗓️ Converter datas de entrada
    inicio = parse_data(data_inicio)
    fim = parse_data(data_fim)

    if not inicio or not fim:
        print("❌ Datas inválidas — operação cancelada.")
        return None  # evita comparar com None

    # 🧹 Converter a coluna 'data_transacao' se ainda não estiver no formato datetime
    df['data_transacao'] = pd.to_datetime(df['data_transacao'], format="%d/%m/%Y", errors='coerce')

    # 🔎 Filtrar pelo período
    filtro = (df['data_transacao'] >= inicio) & (df['data_transacao'] <= fim)
    df_filtrado = df[filtro]

    if df_filtrado.empty:
        print("⚠️ Nenhuma transação encontrada no período informado.")
        return {}

    # Calcular totais por categoria
    totais = df_filtrado.groupby('categoria')['valor'].sum().to_dict()
    return totais

def exibir_extrato(df):
    
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

    print("\n=== 💰 TOTAIS ===")
    print(f"📈 Total de Receitas: R$ {total_receitas:,.2f}")
    print(f"📉 Total de Despesas: R$ {total_despesas:,.2f}")
    print(f"💵 Saldo Atual: R$ {saldo:,.2f}")

def gerar_relatorio_categorias(df, nome_arquivo="relatorio_receitas_despesas.png"):
    if not os.path.exists("relatorios"):
        os.makedirs("relatorios")
    
    plt.figure(figsize=(8,5))
    df.plot(kind='bar', color=['red', 'green'])
    plt.title('Receitas e Despesas por Categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Valor (R$)')
    plt.legend(['Despesas', 'Receitas'])
    plt.tight_layout()
    
    caminho = os.path.join("relatorios", nome_arquivo)
    plt.savefig(caminho)
    plt.show()
    
    print(f"✅ Relatório salvo em '{caminho}'")
