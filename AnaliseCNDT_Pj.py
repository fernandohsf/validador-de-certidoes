import os
import re
import fitz
from datetime import datetime
from MunicipiosPR.Interacoes.validade import verificarDataValidade
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from googleDrive import renomearArquivoDrive

def validarCNDT(service_drive, cliente_gspread, pastaDownload, idPasta, idProfessor, nomeProfessor, planilhaID):
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

        if('CERTIDÃO NEGATIVA DE DÉBITOS TRABALHISTAS' in conteudo):
            valido = 'Sim'
            observacao = ''

            novoNome = f"03-CNDT {nomeProfessor}.pdf"
            novoNome, duplicado = renomearArquivoDrive(service_drive, os.path.splitext(arquivo)[0], novoNome, idPasta)
            if duplicado:
                observacao += 'Existem arquivos de CNDT duplicados. '
                lancamentoControle(idProfessor, 'J', '', observacao, '', '', cliente_gspread, planilhaID)
                continue

            conteudo = re.sub('\xa0', ' ', conteudo)
            conteudo = re.split('\n', conteudo)

            for linha in conteudo:
                if('CNPJ:' in linha or 'CPF:' in linha):
                    cnpj = linha.split(': ')[-1].strip()

                if('Validade:' in linha):
                    dataValidade = linha.split(': ')[-1].strip().split(' - ')[0].strip()
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
            
            try:
                valido = verificarDataValidade(data, dataValidade, valido)
                if(valido == 'Não'):
                    observacao += 'Verificar validade da Certidão CNDT. '
            except:
                continue

            if(len(cnpj) != 18):
                valido = 'Não'
                observacao = observacao + 'Certidão CNDT não é jurídica ou CNPJ inválido. '

            lancamentoControle(idProfessor, 'J', valido, observacao, '', '', cliente_gspread, planilhaID)