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

def validarCRF(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha):
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
            apto = cnpj = dataValidade = diasValidade = codigoValidacao = dataModificacao = observacao = '-'

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
            
            if('Fundo de Garantia do Tempo de Servico - FGTS' in conteudo 
                or 'Certificado de Regularidade do\nFGTS' in conteudo
                or 'Certificado de Regularidade do FGTS' in conteudo
                or 'Certificado de\nRegularidade do FGTS' in conteudo):

                apto = 'Apto'
                valido = 'Sim'
                observacao = ''
                conteudo = re.sub('\xa0', ' ', conteudo)
                conteudo = re.split('\n', conteudo)
                
                for i, linha in enumerate(conteudo):
                    if('Inscrição:' in linha):
                        cnpj = conteudo[i+1].strip()

                    if('Validade:' in linha):
                        dataValidade = linha.strip().split(' ')[-1].strip()
                        dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

                    if('Número:' in linha):
                        codigoValidacao = linha.strip().split(': ')[-1].strip()

                try:
                    diasValidade, dataValidade, apto, valido = verificarDataValidade(data, dataValidade, apto, valido)
                    if(valido == 'Não'):
                        observacao += 'Verificar validade da Certidão CRF. '
                except:
                    continue

                if(len(cnpj) != 18):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Certidão CRF não é jurídica ou CNPJ inválido. '

                dataModificacao = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime(os.path.join(pasta, arquivo)))) 

                nomeBase = f"04-CRF {nomeEmissor}.pdf"
                nomeDocumento, duplicado = renomearArquivoDuplicado(pasta, arquivo, nomeBase)
                
                if duplicado:
                    observacao += 'Existem arquivos de CRF duplicados. '
                
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

                lancamentoControle(id, 'K', valido, observacao ,'', '')

    fecharExcel()