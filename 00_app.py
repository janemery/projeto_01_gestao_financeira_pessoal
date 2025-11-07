from datetime import datetime

'''
inicia o app
mostra o menu
-- escolher tipo [Receita ou despesa]
-- Selecionar o grupo [salario, horas extras, bonificacao, plano de saude, gympass]
-- Informar a data formato (dd/mm/aaaa)

'''

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

            # 🔹 Data (formato YYYY-MM-DD)
            elif campo == 'data':
                valor = input("Digite a data (YYYY-MM-DD): ")
                try:
                    datetime.strptime(valor, "%Y-%m-%d")
                    break
                except ValueError:
                    print("❌ Data inválida! Use o formato YYYY-MM-DD (ex: 2025-11-07).")
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


# 🔹 This part ensures the app starts automatically when run directly
if __name__ == "__main__":
    main()