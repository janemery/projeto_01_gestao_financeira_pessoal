def criar_receita():
    # define the fields that the dictionary should have
    campos = ['tipo', 'descricao', 'valor', 'data']
    
    receita = {}
    
    for campo in campos:
        # Loop until valid input is given
        valor = input(f"Digite o valor para '{campo}': ")
        
        # convert 'valor' field to float automatically
        if campo == 'valor':
            try:
                # Try to convert to float
                    valor = float(valor)
                    break  # ✅ valid, exit the loop
            except ValueError:
                    print("Valor inválido! Informe um número, por exemplo: 5000.00 ou 1234.56.")
                    continue  # ask again
            else:
                # For other fields, just accept the input
                break
        
        receita[campo] = valor
    
    return receita


# print receita
nova_receita = criar_receita()
print("\nDicionário criado:")
print(nova_receita)
