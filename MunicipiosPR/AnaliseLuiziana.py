import re
import locale
from datetime import datetime, timedelta

def validarLuizianaPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if("MUNICIPAL DE LUIZIANA" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF:' in linha):
                cnpj = linha.split(': ')[-1].strip()
            
            if('CPF/CNPJ:' in linha):
                cnpj = conteudo[i+7].strip()

            if('LUIZIANA - PR ,' in linha):
                dataValidade = linha.split(', ')[-1].replace('.', '').strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y') + timedelta(days=90)
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade 
    return '-', '-'