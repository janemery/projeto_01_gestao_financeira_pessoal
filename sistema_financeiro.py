def criar_receita(tipo, descricao, valor, data):
    receita = {
        'tipo': tipo,
        'descricao': descricao,
        'valor': valor,
        'data': data
    }
    return receita

# print minha receita
minha_receita = criar_receita('receita', 'Salário', 5000.00, '2024-01-15')
print(minha_receita)
