import re
from datetime import datetime

def validarSantoAntonioDoSudoestePR(conteudo):
    if("Município de Santo Antonio do Sudoeste" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for linha in conteudo:
            cnpj = 'Inscrição não informa cnpj.'
                
            if("valida até:" in linha):
                dataValidade = linha.split(':')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'