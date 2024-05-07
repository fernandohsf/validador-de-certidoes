import re
from datetime import datetime

def validarSaoJoaoDoIvaiPR(conteudo):
    if('MUNICIPAL DE SÃO JOÃO DO IVAÍ' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF:' in linha):
                cnpj = re.split(': ', linha)[-1].strip()
                
            if('Vencimento:' in linha):
                dataValidade = re.split(':', linha)[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'

        return cnpj, dataValidade
    return '-', '-'