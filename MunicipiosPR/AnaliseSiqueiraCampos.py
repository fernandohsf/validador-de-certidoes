import re
from datetime import datetime

def validarSiqueiraCamposPR(conteudo):

    if("MUNICIPAL SIQUEIRA CAMPOS" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ:' in linha):
                cnpj = linha.split(': ')[-1].strip()
                cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

            if('Inscrição' in linha):
                dataValidade = conteudo[i-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                
        return cnpj, dataValidade 
    return '-', '-'