import re

def identificacao(pastas):
    id = re.split(' - ', pastas)
    id = int(id[0])
    nomeEmissor = re.split(' - ', pastas)
    nomeEmissor = nomeEmissor[-1]
    return id, nomeEmissor