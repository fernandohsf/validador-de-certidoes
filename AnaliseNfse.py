import re
import os
import time
import fitz
from datetime import datetime
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from MunicipiosPR.Excel.ExcelNota import criarExcel, incluirNoExcel, fecharExcel
from MunicipiosPR.Interacoes.identificacao import identificacao

def validarNFSE(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBase):
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
            apto = dataModificacao = observacao = valorNota = cnpj = tomador = cnae = valorNota = chaveAcesso = numeroNota = '-'
            cnpjBase = None

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

            if('Documento Auxiliar da NFS-e' in conteudo):
                apto = 'Apto'
                observacao = ''
                valido = 'Sim'
                observador = 0
                conteudo = re.sub('\xa0', ' ', conteudo)
                conteudo = re.split('\n', conteudo)

                for linha in dadosBase.values():
                    if(int(linha.get('ID')) == id):
                        cnpjBase = linha.get('CNPJ')
                        break
                
                for i, linha in enumerate(conteudo):
                    if ('Chave de Acesso da NFS-e' in linha):
                        chaveAcesso = conteudo[i+1].strip()
                        if(len(chaveAcesso) != 50):
                            chaveAcesso = conteudo[i+3].strip()

                    if('Número da NFS-e' in linha):
                        numeroNota = conteudo[i+1]   

                    if('Prestador do Serviço' in linha):
                        cnpj = conteudo[i+2].strip() 
                        if(len(cnpj) != 18):
                            cnpj = conteudo[i+8]

                    if('TOMADOR DO SERVIÇO' in linha):
                        tomador = conteudo[i+2].strip()
                        if(tomador == '15.513.690/0001-50'):
                            tomador = 'FAPEC'
                        else:
                            apto = 'Inapto'
                            valido = 'Não'
                            tomador = '-'
                            observacao = 'NFS-e sem tomardor ou tomador incorreto. '
                            
                    if('TOMADOR DO SERVIÇO NÃO IDENTIFICADO NA NFS-e' in linha):
                        apto = 'Inapto'
                        tomador = '-'
                        valido = 'Não'
                        observacao = 'NFS-e sem tomardor ou tomador incorreto. '

                    if('Código de Tributação Nacional' in linha):
                        cnae = conteudo[i+1]
                        cnae = re.split(' - ', cnae)[0]
                        if(cnae != '08.02.01'):
                            apto = 'Inapto'
                            valido = 'Não'
                            observacao = observacao + 'CNAE incorreto na NFS-e. '

                    if('Valor Líquido da NFS-e' in linha):
                        valorNota = conteudo[i+1].strip()
                        if(valorNota != 'R$ 1.400,00'):
                            valido = 'Não'
                            observacao = observacao + 'Verificar valor da NFS-e. '

                    if('ATIVIDADES DESCRITAS NA CLÁUSULA PRIMEIRA DO' in linha.upper() 
                       or 'ATIVIDADES DESCRITAS NA CLAUSULA PRIMEIRA DO' in linha.upper()
                       or 'ATIVIDADES DESCRITAS NA CLÁUSULA\nPRIMEIRA DO CONTRATO' in linha.upper()
                       or 'ATIVIDADES DESCRITAS NA CLÁUSULA 1º' in linha.upper()
                       or 'ATIVIDADES DESCRITAS NA CLAUSULA 1º' in linha.upper()):
                        observador += 1
                    if('PERÍODO' in linha.upper()
                       or 'PERIODO' in linha.upper()
                       or 'COMPETÊNCIA' in linha.upper()
                       or 'COMPETENCIA' in linha.upper()):
                        observador += 1
                    if(('AGÊNCIA' in linha.upper() and 'CONTA' in linha.upper())
                       or ('AGENCIA' in linha.upper() and 'CONTA' in linha.upper())
                        or ('AG:' in linha.upper() and 'CONTA' in linha.upper())):
                        observador += 1 

                if(cnpj == ''):
                    observacao = observacao + 'Verificar CNPJ na NFS-e. '

                if(cnpj != cnpjBase):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Verificar CNPJ na NFS-e. '

                if(observador < 3):
                   apto = 'Inapto'
                   valido = 'Não'
                   observacao = 'Verificar a descrição do serviço na NFSE. '

                dataModificacao = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime(os.path.join(pasta, arquivo))))

                try:
                    nomeDocumento = f'01-NFSE {nomeEmissor}.pdf'
                    os.rename(os.path.join(pasta, arquivo), os.path.join(pasta, nomeDocumento))        
                except:
                    nomeDocumento = f'DUPLICADO 01-NFSE {nomeEmissor}.pdf'
                    os.rename(os.path.join(pasta, arquivo), os.path.join(pasta, nomeDocumento))    
                    observacao = observacao + 'Existem dois arquivos de NFSE. ' 
                
                documentoAvaliado = (
                        datetime.strftime(data,'%d/%m/%Y'),
                        nomeDocumento,
                        dataModificacao,
                        id,
                        nomeEmissor,
                        cnpj,
                        chaveAcesso,
                        numeroNota,
                        tomador,
                        cnae,
                        valorNota,
                        apto,
                        observacao
                    )
                linhaExcel +=1
                incluirNoExcel(linhaExcel, 0, documentoAvaliado)

                lancamentoControle(id, 'L', valido, observacao, valorNota, numeroNota)

    fecharExcel()