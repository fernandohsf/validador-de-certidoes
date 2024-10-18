import re
import os
import time
import fitz
from datetime import datetime
from MunicipiosPR.Interacoes.renomearDocumentos import renomearArquivoDuplicado
from MunicipiosPR.Interacoes.validade import verificarDataValidade
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from MunicipiosPR.Excel.ExcelCertidoes import criarExcel, incluirNoExcel, fecharExcel
from MunicipiosPR.Interacoes.identificacao import identificacao

def validarCNDU(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha):
    data = datetime.today()
    diretorioRelatorio = diretorioRelatorio
    nomeRelatorio = nomeRelatorio
    nomePlanilha = nomePlanilha
    criarExcel(f'{diretorioRelatorio}/{nomeRelatorio} - {data.strftime("%d-%m-%Y(%Hh %Mm %Ss)")}.xlsx', nomePlanilha)

    linhaExcel = 0
    for pastas in os.listdir(diretorioAvaliacao):
        pasta = os.path.join(diretorioAvaliacao, pastas)
        id, nomeEmissor = identificacao(pastas)

        for arquivo in os.listdir(pasta):
            apto = cnpj = dataValidade = diasValidade = codigoValidacao = dataModificacao = observacao = valido = '-'

            if not(arquivo.endswith('.pdf') or arquivo.endswith('.PDF')):
                continue

            try:
                pdf = fitz.open(os.path.join(pasta, arquivo))
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
                apto = 'Apto'
                valido = 'Sim'
                observacao = ''
                conteudo = re.sub('\xa0', ' ', conteudo)
                conteudo = re.split('\n', conteudo)

                for linha in conteudo:
                    if('CNPJ:' in linha or 'CPF:' in linha):
                        cnpj = linha.split(': ')[-1].strip()
                        
                    if('Válida até' in linha):  
                        dataValidade = linha.strip().split(' ')[-1].replace('.', '')
                        dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

                    if('Código de controle' in linha):
                        codigoValidacao = linha.split(': ')[-1].strip()

                try:
                    diasValidade, dataValidade, apto, valido = verificarDataValidade(data, dataValidade, apto, valido)
                    if(valido == 'Não'):
                        observacao += 'Verificar validade da Certidão CNDU. '
                except:
                    continue

                if(len(cnpj) != 18):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Certidão CNDU não é jurídica ou CNPJ inválido. '

                nomeDocumento = f'02-CNDU {nomeEmissor}.pdf'

                dataModificacao = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime(os.path.join(pasta, arquivo))))

                nomeBase = f"02-CNDU {nomeEmissor}.pdf"
                nomeDocumento, duplicado = renomearArquivoDuplicado(pasta, arquivo, nomeBase)
                
                if duplicado:
                    observacao += 'Existem arquivos de CNDU duplicados. '
                
                documentoAvaliado = (
                    datetime.strftime(data,'%d/%m/%Y'),
                    nomeDocumento,
                    dataModificacao,
                    id,
                    nomeEmissor,
                    cnpj,
                    codigoValidacao,
                    dataValidade,
                    diasValidade,
                    apto,
                    observacao
                )
                linhaExcel +=1
                incluirNoExcel(linhaExcel, 0, documentoAvaliado)

                lancamentoControle(id, 'I', valido, observacao, '', '')

    fecharExcel()