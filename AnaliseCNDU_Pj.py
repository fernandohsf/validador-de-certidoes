import os
import re
import fitz
from datetime import datetime
from MunicipiosPR.Interacoes.validade import verificarDataValidade
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from googleDrive import renomearArquivoDrive

def validarCNDU(service_drive, cliente_gspread, pastaDownload, idPasta, idProfessor, nomeProfessor, planilhaID):
    data = datetime.today()

    for arquivo in os.listdir(pastaDownload):
        cnpj = dataValidade = observacao = valido = '-'

        try:
            pdf = fitz.open(os.path.join(pastaDownload, arquivo))
            conteudo = ''
            if pdf.page_count != 1:
                continue
            for page in pdf:
                conteudo += page.get_text()
            pdf.close()
        except:
            continue

        if (len(conteudo) < 200):
            continue

        if('CERTIDÃO NEGATIVA DE DÉBITOS RELATIVOS AOS TRIBUTOS FEDERAIS' in conteudo 
        or 'CERTIDÃO POSITIVA COM EFEITOS DE NEGATIVA DE DÉBITOS RELATIVOS AOS TRIBUTOS\nFEDERAIS' in conteudo):
            valido = 'Sim'
            observacao = ''

            novoNome = f"02-CNDU {nomeProfessor}.pdf"
            novoNome, duplicado = renomearArquivoDrive(service_drive, os.path.splitext(arquivo)[0], novoNome, idPasta)
            if duplicado:
                observacao += 'Existem arquivos de CNDU duplicados. '
                lancamentoControle(idProfessor, 'I', '', observacao, '', '', cliente_gspread, planilhaID)
                continue

            conteudo = re.sub('\xa0', ' ', conteudo)
            conteudo = re.split('\n', conteudo)

            for linha in conteudo:
                if('CNPJ:' in linha or 'CPF:' in linha):
                    cnpj = linha.split(': ')[-1].strip()
                    
                if('Válida até' in linha):  
                    dataValidade = linha.strip().split(' ')[-1].replace('.', '')
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

            try:
                valido = verificarDataValidade(data, dataValidade, valido)
                if(valido == 'Não'):
                    observacao += 'Verificar validade da Certidão CNDU. '
            except:
                continue

            if(len(cnpj) != 18):
                valido = 'Não'
                observacao = observacao + 'Certidão CNDU não é jurídica ou CNPJ inválido. '

            lancamentoControle(idProfessor, 'I', valido, observacao, '', '', cliente_gspread, planilhaID)