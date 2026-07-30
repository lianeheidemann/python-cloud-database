"""Cálculos simples de crescimento bacteriano."""


def calcula_bacterias(populacao_inicial, periodos=10):
    """
    Retorna a população bacteriana a cada período.

    O modelo considera que a população dobra em cada período.
    Por exemplo, calcula_bacterias(5, 4) retorna [5, 10, 20, 40].
    """
    if populacao_inicial < 0:
        raise ValueError("A população inicial não pode ser negativa.")

    if periodos < 1:
        raise ValueError("A quantidade de períodos deve ser maior que zero.")

    return [populacao_inicial * (2**periodo) for periodo in range(periodos)]
