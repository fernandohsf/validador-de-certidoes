def identificacao(pasta):
    pasta = pasta.split(' - ')
    id = int(pasta[0])
    nomeEmissor = pasta[1]
    return id, nomeEmissor