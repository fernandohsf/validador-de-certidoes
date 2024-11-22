import os
import re
import fitz
from datetime import datetime
from Utils import verificar_data_validade
from integration.excel_drive import lancamento_controle
from integration.google_drive import renomear_arquivo_drive

def validar_CNDE_PR(service_drive, cliente_gspread, pasta_download, id_pasta, id_professor, nome_professor, planilha_ID):
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

        if('Receita Estadual do Paraná' in conteudo):
            valido = 'Sim'
            observacao = ''

            novo_nome = f"05-CNDE {nome_professor}.pdf"
            novo_nome, duplicado = renomear_arquivo_drive(service_drive, os.path.splitext(arquivo)[0], novo_nome, id_pasta)
            if duplicado:
                observacao += 'Existem arquivos de CNDE duplicados. '
                lancamento_controle(id_professor, 'N', '', observacao, '', '', cliente_gspread, planilha_ID)
                continue
            conteudo = re.sub('\xa0', ' ', conteudo)
            conteudo = re.split('\n', conteudo)

            for i, linha in enumerate(conteudo):
                if('CNPJ/MF:' in linha or 'CPF/MF:' in linha):
                    cnpj = conteudo[i+1]
                    
                if('Válida até' in linha):
                    data_validade = linha.split(' - ')[0].split(' ')[-1].strip()
                    data_validade = datetime.strptime(data_validade,'%d/%m/%Y')

            try:
                valido = verificar_data_validade(data, data_validade, valido)
                if(valido == 'Não'):
                    observacao += 'Verificar validade da Certidão CNDE. '
            except:
                continue
            
            if(len(cnpj) != 18 ):
                valido = 'Não'
                observacao = observacao + 'Certidão CNDE não é jurídica ou CNPJ inválido. '

            lancamento_controle(id_professor, 'N', valido, observacao, '', '', cliente_gspread, planilha_ID)