import os
import re
import fitz
from datetime import datetime
from Utils import verificarDataValidade
from integration.ExcelDrive import lancamentoControle
from integration.googleDrive import renomearArquivoDrive

def validarCNDE_PR(service_drive, cliente_gspread, pastaDownload, idPasta, idProfessor, nomeProfessor, planilhaID):
    data = datetime.today()

    for arquivo in os.listdir(pastaDownload):
        cnpj = dataValidade = observacao = '-'

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

        if('Receita Estadual do Paraná' in conteudo):
            valido = 'Sim'
            observacao = ''

            novoNome = f"05-CNDE {nomeProfessor}.pdf"
            novoNome, duplicado = renomearArquivoDrive(service_drive, os.path.splitext(arquivo)[0], novoNome, idPasta)
            if duplicado:
                observacao += 'Existem arquivos de CNDE duplicados. '
                lancamentoControle(idProfessor, 'N', '', observacao, '', '', cliente_gspread, planilhaID)
                continue
            conteudo = re.sub('\xa0', ' ', conteudo)
            conteudo = re.split('\n', conteudo)

            for i, linha in enumerate(conteudo):
                if('CNPJ/MF:' in linha or 'CPF/MF:' in linha):
                    cnpj = conteudo[i+1]
                    
                if('Válida até' in linha):
                    dataValidade = linha.split(' - ')[0].split(' ')[-1].strip()
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

            try:
                valido = verificarDataValidade(data, dataValidade, valido)
                if(valido == 'Não'):
                    observacao += 'Verificar validade da Certidão CNDE. '
            except:
                continue
            
            if(len(cnpj) != 18 ):
                valido = 'Não'
                observacao = observacao + 'Certidão CNDE não é jurídica ou CNPJ inválido. '

            lancamentoControle(idProfessor, 'N', valido, observacao, '', '', cliente_gspread, planilhaID)