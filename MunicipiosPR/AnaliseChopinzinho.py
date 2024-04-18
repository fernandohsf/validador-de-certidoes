import re
from datetime import datetime, timedelta

def validarChopinzinhoPR(conteudo):
    if("www.chopinzinho.pr.gov.br" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ' in linha):
                cnpj = linha.split(': ')[1].replace(' ', '').replace('RG/Inscr....', '').strip()
                
            if("Emitida em" in linha):
                dataValidade = linha.split(' ')[-1].replace('.', '').strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y') + timedelta(days=60)
                
        return cnpj, dataValidade
    return '-', '-'