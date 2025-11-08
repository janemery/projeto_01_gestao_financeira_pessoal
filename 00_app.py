from datetime import datetime
import pandas as pd

'''
inicia o app
mostra o menu
-- escolher tipo [Receita ou despesa]
-- Selecionar o grupo [salario, horas extras, bonificacao, plano de saude, gympass]
-- Informar a data formato (dd/mm/aaaa)

'''
transacoes = []  # <--- inicializa a lista

# Cria o DataFrame a partir da lista de registros
df = pd.DataFrame(transacoes)
df["data"] = pd.to_datetime(df["data"])

def adiciona_registro():
    """
    Cadastra um novo registro financeiro (receita ou despesa).
    Retorna um dicionário com os campos: tipo, descricao, valor e data.
    """
    campos = ['tipo', 'descricao', 'valor', 'data']
    registro = {}

    print("\n=== CADASTRO DE REGISTRO FINANCEIRO ===")

    for campo in campos:
        while True:
            # 🔹 Escolha do tipo: receita ou despesa
            if campo == 'tipo':
                print("\nSelecione o tipo:")
                print("1. Receita")
                print("2. Despesa")
                escolha = input("Digite o número correspondente (1 ou 2): ")

                if escolha == '1':
                    valor = 'receita'
                    break
                elif escolha == '2':
                    valor = 'despesa'
                    break
                else:
                    print("❌ Opção inválida! Digite apenas 1 ou 2.")
                    continue

            # 🔹 Valor numérico
            elif campo == 'valor':
                valor = input("Digite o valor (ex: 5000.00): ").replace(',', '.')
                try:
                    valor = float(valor)
                    break
                except ValueError:
                    print("❌ Valor inválido! Informe um número válido (ex: 1200.50).")
                    continue

            # 🔹 Data (formato DD/MM/YY)
            elif campo == 'data':
                valor = input("Digite a data (DD/MM/AA): ")
                try:
                    # tenta converter no formato dia/mês/ano com 2 dígitos
                    datetime.strptime(valor, "%d/%m/%y")
                    break
                except ValueError:
                    print("❌ Data inválida! Use o formato DD/MM/AA (ex: 01/02/25).")
                    continue

            # 🔹 Descrição
            else:
                valor = input("Digite a descrição: ").strip()
                if valor == "":
                    print("❌ A descrição não pode ficar vazia.")
                    continue
                break

        registro[campo] = valor

    print("\n✅ Registro adicionado com sucesso!")
    return registro


def calcular_saldos_pandas(df, inicio=None, fim=None):
    """Calcula saldos totais e por categoria usando pandas."""
    if "data" not in df.columns:
        raise KeyError("A coluna 'data' não existe no DataFrame.")
    
    filtro = pd.Series(True, index=df.index)
    if inicio:
        filtro &= df["data"] >= pd.to_datetime(inicio)
    if fim:
        filtro &= df["data"] <= pd.to_datetime(fim)
    
    df_filtrado = df[filtro]

    total_receitas = df_filtrado[df_filtrado["tipo"] == "receita"]["valor"].sum()
    total_despesas = df_filtrado[df_filtrado["tipo"] == "despesa"]["valor"].sum()
    
    # Agrupar despesas por categoria
    if "categoria" in df_filtrado.columns:
        gastos_por_categoria = (
            df_filtrado[df_filtrado["tipo"] == "despesa"]
            .groupby("categoria")["valor"]
            .sum()
            .to_dict()
        )
    else:
        gastos_por_categoria = {}

    saldo_atual = total_receitas - total_despesas
    return saldo_atual, total_receitas, total_despesas, gastos_por_categoria

saldo2, receitas2, despesas2, categorias2 = calcular_saldos_pandas(df)
print("Saldo atual (pandas):", saldo2)
print("Receitas:", receitas2)
print("Despesas:", despesas2)
print("Gastos por categoria:", categorias2)


def menu():
    print("\n===========================")
    print("   💰 GERENCIADOR FINANCEIRO")
    print("===========================")
    print("1. Adicionar registro")
    print("2. Listar registros")
    print("3. Sair")

    while True:
        opcao = input("Escolha uma opção (1-3): ")
        if opcao in ['1', '2', '3']:
            return opcao
        else:
            print("❌ Opção inválida! Escolha um número entre 1 e 3.")


def main():
    registros = []

    while True:
        opcao = menu()

        if opcao == '1':
            novo_registro = adiciona_registro()
            registros.append(novo_registro)

        elif opcao == '2':
            print("\n=== LISTA DE REGISTROS ===")
            if registros:
                for i, r in enumerate(registros, start=1):
                    print(f"{i}. Tipo: {r['tipo']} | Descrição: {r['descricao']} | Valor: {r['valor']:.2f} | Data: {r['data']}")
            else:
                print("Nenhum registro cadastrado ainda.")

        elif opcao == '3':
            print("\n👋 Saindo... Até logo!")
            break


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
# 🔹 This part ensures the app starts automatically when run directly
if __name__ == "__main__":
    main()

    transacoes = []

    while True:
        registro = adiciona_registro()
        transacoes.append(registro)

        continuar = input("\nDeseja adicionar outro registro? (s/n): ").strip().lower()
        if continuar != "s":
            break

    # Criação do DataFrame
    df = pd.DataFrame(transacoes)
    print("\n📊 DataFrame criado com sucesso!")
    print(df)

    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%y", errors="coerce")

    # Calcular saldos
    saldo, receitas, despesas, categorias = calcular_saldos_pandas(df)

    print("\n=== RELATÓRIO FINANCEIRO ===")
    print(f"💰 Saldo atual: R$ {saldo:,.2f}")
    print(f"📈 Total de receitas: R$ {receitas:,.2f}")
    print(f"📉 Total de despesas: R$ {despesas:,.2f}")
    print("🏷️ Gastos por categoria:")
    for cat, val in categorias.items():
        print(f"   - {cat}: R$ {val:,.2f}")