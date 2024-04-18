import re
from datetime import datetime

def validarRibeiraoClaroPR(conteudo):
    if('MUNICIPIO DE RIBEIRAO CLARO' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for linha in conteudo:
            if('CPF/CNPJ' in linha):
                cnpj = linha.split(' nº ')[-1].replace('.', '').replace('/', '').replace('-', '').strip()
                cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
            
            if('validade até:' in linha):
                dataValidade = linha.split(': ')[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y.')
                
        return cnpj, dataValidade
    return '-', '-'