import logging

from financeiro.csv import validar_csv
from financeiro.extrato import (
    calcular_saldo,
    exibir_total_categorias_periodo,
    exibir_extrato,
    resumo_financeiro,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


def menu():
    """
    Exibe o menu principal do sistema e solicita uma opção do usuário.

    Returns:
        str: O número da opção escolhida, entre "1", "2", "3" ou "4".

    Notas:
        A função só retorna quando o usuário informa uma opção válida.
    """
    print("\n===============================")
    print("GERENCIADOR FINANCEIRO PESSOAL")
    print("===============================")

    print("1 - Exibir extrato completo")
    print("2 - Mostrar resumo financeiro")
    print("3 - Mostrar total de categorias por período")
    print("4 - Sair")
    print("===============================")

    while True:
        opcao = input("Escolha uma opção (1-4): ").strip()
        if opcao in ["1", "2", "3", "4"]:
            return opcao
        print("Opção inválida! Tente novamente.")


def main():
    """
    Função principal do sistema financeiro.

    Responsável por:
      - Validar o arquivo CSV de dados financeiros;
      - Carregar o DataFrame principal;
      - Exibir o menu interativo;
      - Encaminhar o usuário para as funções adequadas;
      - Controlar o fluxo principal da aplicação.

    Fluxo:
        1. Valida o arquivo CSV.
        2. Calcula o saldo inicial.
        3. Entra no menu principal e executa ações conforme a opção escolhida.

    Erros:
        Caso o arquivo CSV seja inválido ou não possa ser lido,
        a execução é encerrada de forma segura.

    Returns:
        None
    """
    arquivo = "dados_financeiros.csv"

    try:
        df = validar_csv(arquivo)
    except Exception as exc:
        logger.error("Erro ao validar CSV: %s", exc)
        return

    if df is None:
        logger.error("Arquivo inválido. Encerrando execução.")
        return

    saldo = calcular_saldo(df)
    if saldo is not None:
        logger.info("Saldo atual carregado com sucesso.")

    while True:
        opcao = menu()

        if opcao == "1":
            exibir_extrato(df)

        elif opcao == "2":
            resumo_financeiro(df)

        elif opcao == "3":
            exibir_total_categorias_periodo(df)

        elif opcao == "4":
            print("\nSaindo... Até logo.")
            break


if __name__ == "__main__":
    main()
