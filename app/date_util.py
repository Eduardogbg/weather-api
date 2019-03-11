"""
    Opera com strings YYYY-mm-dd
"""
from datetime import datetime

def today():
    return datetime.today().strftime('%Y-%m-%d')

def days_diff(a, b):
    """
        Sendo 'a' uma data inicial e 'b' final, retorna a diferença de 
        'b' para 'a'. Note que caso 'a' seja uma data posterior a 'b',
        o resultado será negativo
    """
    a = datetime.strptime(a, '%Y-%m-%d')
    b = datetime.strptime(b, '%Y-%m-%d')
    return (b - a).days

def is_between(c, a, b):
    """
        Verifica se uma data 'c' está no intervalo [a, b].
        Faz isso através do sinal da diferença entre as datas
    """
    backw = days_diff(a, c)
    forw = days_diff(c, b)

    return backw*forw >= 0
