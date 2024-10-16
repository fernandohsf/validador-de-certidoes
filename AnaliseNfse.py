import re
import os
import time
import fitz
import calendar
from datetime import datetime
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from MunicipiosPR.Excel.ExcelNota import criarExcel, incluirNoExcel, fecharExcel
from MunicipiosPR.Interacoes.identificacao import identificacao
from MunicipiosPR.Interacoes.renomearDocumentos import renomearArquivoDuplicado

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
            cnpjBase = valorReceber = None

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
                observadorClausula = observadorPeriodo = observadorConta = 0
                conteudo = re.sub('\xa0', ' ', conteudo)
                conteudo = re.split('\n', conteudo)

                for id_linha, linha in dadosBase.items():
                    if(int(id_linha) == id):
                        cnpjBase = linha.get('CNPJ')
                        valorReceber = linha.get('Valor a receber')
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
                            endereco = (conteudo[i+12].strip(), conteudo[i+14].strip(), conteudo[i+16].strip())
                            enderecos_validos = [
                                ('GOIAS, 587, JARDIM DOS ESTADOS', 'Campo Grande - MS', '79020-100'),
                                ('R GOIAS, 587, JARDIM DOS ESTADOS', 'Campo Grande - MS', '79020-100')
                            ]

                            if endereco not in enderecos_validos:
                                observacao += 'Endereço do tomador incorreto. '

                        else:
                            apto = 'Inapto'
                            valido = 'Não'
                            tomador = '-'
                            observacao = observacao + 'NFS-e sem tomador ou tomador incorreto. '
                            
                    if('TOMADOR DO SERVIÇO NÃO IDENTIFICADO NA NFS-e' in linha):
                        apto = 'Inapto'
                        tomador = '-'
                        valido = 'Não'
                        observacao = observacao + 'NFS-e sem tomador ou tomador incorreto. '

                    if('Código de Tributação Nacional' in linha):
                        cnae = conteudo[i+1]
                        cnae = re.split(' - ', cnae)[0]
                        if(cnae != '08.02.01'):
                            apto = 'Inapto'
                            valido = 'Não'
                            observacao = observacao + 'CNAE incorreto na NFS-e. '

                    if('Valor Líquido da NFS-e' in linha):
                        valorNota = conteudo[i+1].split(' ')[-1].replace('.', '').replace(',', '.').strip()
                        if(valorReceber is not None):
                            valorReceber = valorReceber.replace('.', '').replace(',', '.').strip()
                            if(float(valorNota) != float(valorReceber)):
                                valido = 'Não'
                                observacao = observacao + 'O valor total da nota difere do valor cadastrado. '
                        else:
                            observacao = observacao + 'Sem valor cadastrado na planilha. '

                    if('ATIVIDADES DESCRITAS NA CLÁUSULA PRIMEIRA D' in linha.upper() 
                       or 'ATIVIDADES DESCRITAS NA CLAUSULA PRIMEIRA D' in linha.upper()
                       or 'ATIVIDADES DESCRITAS NA CLÁUSULA\nPRIMEIRA DO CONTRATO' in linha.upper()
                       or 'ATIVIDADES DESCRITAS NA CLÁUSULA 1º' in linha.upper()
                       or 'ATIVIDADES DESCRITAS NA CLAUSULA 1º' in linha.upper()
                       or 'DESCRITAS NA CLÁUSULA PRIMEIRA DO CONTRATO' in linha.upper()
                       or 'DESCRITAS NA CLAUSULA PRIMEIRA DO CONTRATO' in linha.upper()
                       or 'DESCRITO NA CLAUSULA PRIMEIRA DO CONTRATO' in linha.upper()):
                        observadorClausula += 1

                    if('PERÍODO DE REALIZAÇÃO' in linha.upper()
                       or 'PERIODO DE REALIZAÇÃO' in linha.upper()
                       or 'PERIODO D REALIZAÇÃO' in linha.upper()
                       or 'COMPETÊNCIA:' in linha.upper()
                       or 'COMPETENCIA:' in linha.upper()):
                        linha = linha.upper()
                        periodo = linha.split('AÇÃO: ')[-1].split('.')[0].split(',')[0].upper()
                        periodo = periodo.replace(' ', '')
                        mes = data.month - 1
                        ano = data.year

                        if(mes == 0):
                            mes = 12
                            ano -=1
                        mesAnterior = datetime(ano, mes, 1)
                        finalMesAnterior = datetime(ano, mes, calendar.monthrange(ano, mes)[1])

                        if(mesAnterior.strftime('%BDE%Y').upper() in periodo
                        or mesAnterior.strftime('%B%Y').upper() in periodo
                        or f'{mesAnterior.strftime("%d/%m/%Y")}A{finalMesAnterior.strftime("%d/%m/%Y")}' in periodo
                        or f'{mesAnterior.strftime("%d/%m/%Y")}À{finalMesAnterior.strftime("%d/%m/%Y")}' in periodo
                        or f'{mesAnterior.strftime("%d/%m/%Y")}Á{finalMesAnterior.strftime("%d/%m/%Y")}' in periodo
                        or f'{mesAnterior.strftime("%d/%m/%Y")}ATÉ{finalMesAnterior.strftime("%d/%m/%Y")}' in periodo
                        or f'{mesAnterior.strftime("%d/%m")}A{finalMesAnterior.strftime("%d/%mDE%Y")}' in periodo):
                            observadorPeriodo += 1

                    if('AGÊNCIA' in linha.upper() or 'AGENCIA' in linha.upper() or 'AG:' in linha.upper()):
                        conta = conteudo[i:i+3]
                        for linha2 in conta:
                            if('CONTA' in linha2.upper()):
                                observadorConta += 1 

                if(cnpj == ''):
                    observacao = observacao + 'Verificar CNPJ na NFS-e. '

                if(cnpj != cnpjBase):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Verificar CNPJ na NFS-e. '

                if(observadorClausula == 0):
                   apto = 'Inapto'
                   valido = 'Não'
                   observacao = observacao + 'Verificar a referência a cláusula do contrato na descrição da NFSE. '
                
                if(observadorPeriodo == 0):
                   apto = 'Inapto'
                   valido = 'Não'
                   observacao = observacao + 'Verificar o período de realização na descrição da NFS-e.'

                if(observadorConta == 0):
                   apto = 'Inapto'
                   valido = 'Não'
                   observacao = observacao + 'Verificar a agência e conta na descrição da NFS-e.'

                dataModificacao = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime(os.path.join(pasta, arquivo))))


                nomeBase = f"01-NFSE {nomeEmissor}.pdf"
                nomeDocumento, duplicado = renomearArquivoDuplicado(pasta, arquivo, nomeBase)
                
                if duplicado:
                    observacao += 'Existem arquivos de NFSE duplicados. '
                
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