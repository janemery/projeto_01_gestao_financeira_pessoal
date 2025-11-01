def criar_receita():
    # define the fields that the dictionary should have
    campos = ['tipo', 'descricao', 'valor', 'data']
    
    receita = {}
    
    for campo in campos:
        valor = input(f"Digite o valor para '{campo}': ")
        
        # convert 'valor' field to float automatically
        if campo == 'valor':
            try:
                valor = float(valor)
            except ValueError:
                print("Valor inválido. Definindo como 0.0")
                valor = 0.0
        
        receita[campo] = valor
    
    return receita


# Exemplo de uso
nova_receita = criar_receita()
print("\nDicionário criado:")
print(nova_receita)
