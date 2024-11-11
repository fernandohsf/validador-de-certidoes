import os
import re
import fitz
from datetime import datetime
from MunicipiosPR.Interacoes.validade import verificarDataValidade
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from googleDrive import renomearArquivoDrive

def validarCRF(service_drive, cliente_gspread, pastaDownload, idPasta, idProfessor, nomeProfessor, planilhaID):
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
        
        if('Fundo de Garantia do Tempo de Servico - FGTS' in conteudo 
            or 'Certificado de Regularidade do\nFGTS' in conteudo
            or 'Certificado de Regularidade do FGTS' in conteudo
            or 'Certificado de\nRegularidade do FGTS' in conteudo):
            valido = 'Sim'
            observacao = ''

            novoNome = f"04-CRF {nomeProfessor}.pdf"
            novoNome, duplicado = renomearArquivoDrive(service_drive, os.path.splitext(arquivo)[0], novoNome, idPasta)
            if duplicado:
                observacao += 'Existem arquivos de CRF duplicados. '
                lancamentoControle(idProfessor, 'K', '', observacao, '', '', cliente_gspread, planilhaID)
                continue

            conteudo = re.sub('\xa0', ' ', conteudo)
            conteudo = re.split('\n', conteudo)
            
            for i, linha in enumerate(conteudo):
                if('Inscrição:' in linha):
                    cnpj = conteudo[i+1].strip()

                if('Validade:' in linha):
                    dataValidade = linha.strip().split(' ')[-1].strip()
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

            try:
                valido = verificarDataValidade(data, dataValidade, valido)
                if(valido == 'Não'):
                    observacao += 'Verificar validade da Certidão CRF. '
            except:
                continue

            if(len(cnpj) != 18):
                valido = 'Não'
                observacao = observacao + 'Certidão CRF não é jurídica ou CNPJ inválido. '

            lancamentoControle(idProfessor, 'K', valido, observacao ,'', '', cliente_gspread, planilhaID)