import os
import re
import fitz
from datetime import datetime
from Utils import verificar_data_validade
from integration.excel_drive import lancamento_controle
from integration.google_drive import renomear_arquivo_drive

def validar_CNDT(service_drive, cliente_gspread, pasta_download, id_pasta, id_professor, nome_professor, planilha_ID):
    data = datetime.today()

    for arquivo in os.listdir(pasta_download):
        cnpj = data_validade = observacao = '-'

        try:
            pdf = fitz.open(os.path.join(pasta_download, arquivo))
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

            novo_nome = f"03-CNDT {nome_professor}.pdf"
            novo_nome, duplicado = renomear_arquivo_drive(service_drive, os.path.splitext(arquivo)[0], novo_nome, id_pasta)
            if duplicado:
                observacao += 'Existem arquivos de CNDT duplicados. '
                lancamento_controle(id_professor, 'J', '', observacao, '', '', cliente_gspread, planilha_ID)
                continue

            conteudo = re.sub('\xa0', ' ', conteudo)
            conteudo = re.split('\n', conteudo)

            for linha in conteudo:
                if('CNPJ:' in linha or 'CPF:' in linha):
                    cnpj = linha.split(': ')[-1].strip()

                if('Validade:' in linha):
                    data_validade = linha.split(': ')[-1].strip().split(' - ')[0].strip()
                    data_validade = datetime.strptime(data_validade,'%d/%m/%Y')
            
            try:
                valido = verificar_data_validade(data, data_validade, valido)
                if(valido == 'Não'):
                    observacao += 'Verificar validade da Certidão CNDT. '
            except:
                continue

            if(len(cnpj) != 18):
                valido = 'Não'
                observacao = observacao + 'Certidão CNDT não é jurídica ou CNPJ inválido. '

            lancamento_controle(id_professor, 'J', valido, observacao, '', '', cliente_gspread, planilha_ID)