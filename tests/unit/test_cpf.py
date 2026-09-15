from src.auth.cpf import validar_cpf, limpar_cpf

def test_limpar_cpf():
    assert limpar_cpf("123.456.789-00") == "12345678900"
    assert limpar_cpf("12345678900") == "12345678900"
    assert limpar_cpf("") == ""

def test_validar_cpf_valido():
    # CPFs validos gerados
    assert validar_cpf("52998224725") is True
    assert validar_cpf("529.982.247-25") is True

def test_validar_cpf_invalido():
    assert validar_cpf("11111111111") is False
    assert validar_cpf("12345678900") is False
    assert validar_cpf("123") is False
    assert validar_cpf("") is False
