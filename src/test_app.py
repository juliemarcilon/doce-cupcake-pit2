from models import calcular_totais_carrinho

def test_calculo_carrinho_com_itens():
    itens = [
        {'preco': 10.00, 'quantidade': 2},  # 20.00
        {'preco': 12.00, 'quantidade': 1},  # 12.00
        {'preco': 11.00, 'quantidade': 1}   # 11.00
    ]
    resultado = calcular_totais_carrinho(itens)
    assert resultado['subtotal'] == 43.00
    assert resultado['frete'] == 8.00
    assert resultado['total'] == 51.00

def test_calculo_carrinho_vazio():
    resultado = calcular_totais_carrinho([])
    assert resultado['subtotal'] == 0.00
    assert resultado['frete'] == 0.00
    assert resultado['total'] == 0.00