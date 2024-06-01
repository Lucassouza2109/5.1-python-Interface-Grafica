
import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')
# NUMERO OU PONTO = RE (EXPRESAO REGULAR) COMPILANDO 
# TUDO QUE ESTIVER ENTRE 0-9 OU PONTO


def isNumOrDot(string: str): # SE FOR NUMERO OU PONTO. 
    return bool(NUM_OR_DOT_REGEX.search(string))

def converToNumber(string: str):
    number = float(string)

    if number.is_integer():
        number = int(number)

    return number


def isValidNumber(string: str): 
    # FORMULA PARA VALIDACAO : SE A STRING INFORMADA FOR UM NUMERO VALIDO.
    valid = False
    try: # TENTE CONVERTER A MINHA STRING PARA FLOAT. 
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid



def isEmpty(string: str): # VERIFICA SE O CAMPO ESTA VAZIO. 
    return len(string) == 0