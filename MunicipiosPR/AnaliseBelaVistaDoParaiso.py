import re
from datetime import datetime

def validarBelaVistaDoParaisoPR(conteudo):

    if("MUNICIPAL DE BELA VISTA DO PARAISO" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for linha in conteudo:
            if('CPF/CNPJ' in linha):
                cnpj = linha.split('nº ')[-1].replace('.', '').replace('/', '').replace('-', '').strip()
                cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

            if('VALIDADE ATÉ' in linha):
                dataValidade = linha.split('ATÉ ')[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                
        return cnpj, dataValidade 
    return '-', '-'