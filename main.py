from novo_sistema_financeiro import validar_csv
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

    while True:
        opcao = menu()

        if opcao == '1':
            # Exibir extrato
            exibir_extrato(df)

        elif opcao == '2':
            # Resumo geral
            # resumo = calcular_resumo(df)
            totais_categoria = total_por_categoria(df)
            print(totais_categoria)

        elif opcao == '3':
            # Totais por período
            data_inicio = input("📅 Informe a data inicial (dd/mm/aaaa): ")
            data_fim = input("📅 Informe a data final (dd/mm/aaaa): ")

            totais_periodo = total_categorias_por_periodo(df, data_inicio, data_fim)

            print("\n🏷️  Totais por Categoria no Período:")
            for categoria, valor in totais_periodo.items():
                print(f"   - {categoria:<15}: R$ {valor:,.2f}")

        elif opcao == '4':
            print("\n👋 Saindo... Até logo!")
            break


if __name__ == "__main__":
    main()
