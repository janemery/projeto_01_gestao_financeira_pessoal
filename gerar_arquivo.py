import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def gerar_dados_financeiros_csv(nome_arquivo='dados_financeiros_2025.csv', n=100):
    """
    Gera um arquivo CSV com registros financeiros simulados distribuídos em 2025.
    """

    # Definir possíveis categorias e descrições
    categorias_receita = ['Trabalho', 'Serviços', 'Investimentos', 'Outros']
    descricoes_receita = ['Salário', 'Freelance', 'Rendimento', 'Venda equipamento', 'Premiação']

    categorias_despesa = ['Alimentação', 'Contas', 'Saúde', 'Transporte', 'Lazer']
    descricoes_despesa = ['Supermercado', 'Conta de luz', 'Internet', 'Restaurante', 'Farmácia', 'Cinema']

    registros = []
    data_inicio = datetime(2025, 1, 1)
    data_fim = datetime(2025, 12, 31)

    for i in range(n):
        # Alterna entre receita e despesa
        tipo = random.choice([1, 0])

        # Gera uma data aleatória em 2025
        dias_aleatorios = random.randint(0, (data_fim - data_inicio).days)
        data_transacao = (data_inicio + timedelta(days=dias_aleatorios)).strftime("%d/%m/%Y")

        # Gera valores e campos
        if tipo == 1:
            categoria = random.choice(categorias_receita)
            descricao = random.choice(descricoes_receita)
            valor = round(random.uniform(200, 8000), 2)
        else:
            categoria = random.choice(categorias_despesa)
            descricao = random.choice(descricoes_despesa)
            valor = round(random.uniform(20, 1200), 2)

        registros.append({
            'receita_despesa': tipo,
            'data_transacao': data_transacao,
            'valor': valor,
            'descricao': descricao,
            'categoria': categoria
        })

    # Cria o DataFrame
    df = pd.DataFrame(registros)

    # Ordena por data
    df = df.sort_values(by='data_transacao')

    # Salva em CSV
    df.to_csv(nome_arquivo, index=False, encoding='utf-8')

    print(f"✅ Arquivo '{nome_arquivo}' criado com sucesso com {len(df)} registros!")

# Executa a função
gerar_dados_financeiros_csv()
