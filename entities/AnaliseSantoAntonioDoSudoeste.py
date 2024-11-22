import re
from datetime import datetime

def validarSantoAntonioDoSudoestePR(conteudo):
    if("Santo Antônio do Sudoeste" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if 'CNPJ/CPF' in linha:
                cnpj = conteudo[i+1].strip()
                
            if("VALIDADE ATÉ" in linha):
                dataValidade = ''.join(conteudo[i:i+4])
                dataValidade = dataValidade.split('2.')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'                
        return cnpj, dataValidade
    return '-', '-'