from datetime import datetime

'''
inicia o app
mostra o menu
-- escolher tipo [Receita ou despesa]
-- Selecionar o grupo [salario, horas extras, bonificacao, plano de saude, gympass]
-- Informar a data formato (dd/mm/aaaa)

'''

def criar_receita():
    campos = ['tipo (receita ou despesa)', 'descricao', 'valor', 'data']
    receita = {}

    print("\n=== CADASTRO DE RECEITA ===")

    for campo in campos:
        while True:
            valor = input(f"Digite o valor para '{campo}': ")

            # 🔸 Validate tipo (must be 'receita' or 'despesa')
            if campo == 'tipo':
                valor = input(f"Preencha 'receita' ou 'despesa': ")

                if valor.lower() in ['receita', 'despesa']:
                    valor = valor.lower()  # normalize to lowercase
                    break
                else:
                    print("❌ Tipo inválido! Escolha entre 'receita' ou 'despesa'.")
                    continue
            
            if campo == 'valor':
                try:
                    valor = float(valor)
                    break
                except ValueError:
                    print("❌ Valor inválido! Informe um número, por exemplo: 5000.00 ou 1234.56.")
                    continue

            elif campo == 'data':
                try:
                    datetime.strptime(valor, "%Y-%m-%d")
                    break
                except ValueError:
                    print("❌ Data inválida! Use o formato YYYY-MM-DD (exemplo: 2024-01-15).")
                    continue

            else:
                break

        receita[campo] = valor

    return receita


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
    receitas = []

    while True:
        opcao = menu()

        if opcao == '1':
            nova_receita = criar_receita()
            receitas.append(nova_receita)
            print("\n✅ Receita adicionada com sucesso!")

        elif opcao == '2':
            print("\n=== LISTA DE RECEITAS ===")
            if receitas:
                for i, r in enumerate(receitas, start=1):
                    print(f"{i}. Tipo: {r['tipo']} | Descrição: {r['descricao']} | Valor: {r['valor']:.2f} | Data: {r['data']}")
            else:
                print("Nenhuma receita cadastrada ainda.")

        elif opcao == '3':
            print("\n👋 Saindo... Até logo!")
            break


# 🔹 This part ensures the app starts automatically when run directly
if __name__ == "__main__":
    main()