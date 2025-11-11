from novo_sistema_financeiro import calcular_despesas, calcular_receitas, calcular_saldo, validar_csv
from novo_sistema_financeiro import (
    total_por_categoria,
    total_categorias_por_periodo
)
from novo_sistema_financeiro import (
    exibir_extrato
)

def menu():
    """Mostra o menu principal e retorna a escolha do usuário."""
    print("\n===============================")
    print("💰 GERENCIADOR FINANCEIRO PESSOAL")
    print("===============================")
       
    print("1️⃣  Exibir extrato completo")
    print("2️⃣  Mostrar resumo financeiro")
    print("3️⃣  Mostrar total de categorias por período")
    print("4️⃣  Sair")
    print("===============================")

    while True:
        opcao = input("👉 Escolha uma opção (1-4): ").strip()
        if opcao in ['1', '2', '3', '4']:
            return opcao
        else:
            print("❌ Opção inválida! Tente novamente.")

def main():
    """Função principal do sistema financeiro."""
    arquivo = "dados_financeiros.csv"

    try:
        df = validar_csv(arquivo)
    except Exception as e:
        print(e)
        return
    
    # Exibe um resumo inicial
    # print("\n✅ Arquivo carregado com sucesso!")
    # print(df.head(), "\n")

    saldo = calcular_saldo(df)
    # if saldo is not None:
        # print(f"💰 Saldo atual: R$ {saldo:,.2f}")

    # ======================================================
    # MENU PRINCIPAL
    # ======================================================
    while True:
        opcao = menu()

        if opcao == '1':
            # Exibir extrato
            print("\n🏷️  Você escolheu exibir Extrato:")
            exibir_extrato(df)

        elif opcao == '2':
            # Mostrar total por categoria
            totais_categoria = total_por_categoria(df)
            print("\n🏷️  Você escolheu Resumo financeiro:")
            total_receitas = calcular_receitas(df)
            print(f"\n🏷️ Total de receitas: {total_receitas:,.2f}")
            print("\n🏷️ Total por categoria:")
            for cat, val in totais_categoria.items():
                print(f"   - {cat:<15}: R$ {val:,.2f}")
            total_despesas = calcular_despesas(df)
            print("-----------------------------")
            print(f"   Total de despesas: R$ {total_despesas:,.2f}")

        elif opcao == '3':
            # Totais por período
            data_inicio = input("📅 Informe a data inicial (dd/mm/aaaa): ")
            data_fim = input("📅 Informe a data final (dd/mm/aaaa): ")

            totais_periodo = total_categorias_por_periodo(df, data_inicio, data_fim)

            if totais_periodo is None or not totais_periodo:
                print("❌ Não foi possível calcular os totais — verifique as datas ou se há dados no período.")
            else:
                print("\n🏷️  Você escolheu Totais por Categoria no Período:")
                print(f"📅 Período: {data_inicio} - {data_fim}\n")
                for categoria, valor in totais_periodo.items():
                    print(f"   - {categoria:<15}: R$ {valor:,.2f}")
        elif opcao == '4':
            print("\n👋 Saindo... Até logo!")
            break


if __name__ == "__main__":
    main()
