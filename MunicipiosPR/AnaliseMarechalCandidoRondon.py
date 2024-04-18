import re
import locale
from datetime import datetime, timedelta

def validarMarechalCandidoRondonPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    if("MUNICÍPIO DE MARECHAL CÂNDIDO RONDON" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ' in linha):
                cnpj = conteudo[i+1].strip()
                
            if("MARECHAL CÂNDIDO RONDON," in linha):
                dataValidade = linha.split(', ')[-1].replace('.', '').strip()
                dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y') + timedelta(days=60)
        
        return cnpj, dataValidade
    return '-', '-'