import os

def renomearArquivoDuplicado(pasta, arquivo, nomeBase):
    contador = 1
    nomeOriginal = nomeBase
    arquivoNovo = os.path.join(pasta, nomeBase)
    
    while os.path.exists(arquivoNovo):
        nomeBase = f"DUPLICADO_{contador} - {nomeOriginal}"
        arquivoNovo = os.path.join(pasta, nomeBase)
        contador += 1

    os.rename(os.path.join(pasta, arquivo), arquivoNovo)

    return nomeBase, contador > 1