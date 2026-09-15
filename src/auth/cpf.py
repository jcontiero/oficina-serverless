import re

def limpar_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf or "")

def validar_cpf(cpf: str) -> bool:
    cpf_limpo = limpar_cpf(cpf)
    if len(cpf_limpo) != 11:
        return False
    if len(set(cpf_limpo)) == 1:
        return False

    # Primeiro digito verificador
    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    d1 = 0 if resto == 10 else resto
    if int(cpf_limpo[9]) != d1:
        return False

    # Segundo digito verificador
    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    d2 = 0 if resto == 10 else resto
    return int(cpf_limpo[10]) == d2
