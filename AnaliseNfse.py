import os
import re
import fitz
import calendar
from datetime import datetime
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from googleDrive import renomearArquivoDrive

def validarNFSE(service_drive, cliente_gspread, dadosBaseCadastro, pastaDownload, idPasta, idProfessor, nomeProfessor, planilhaID):
    data = datetime.today()

    for arquivo in os.listdir(pastaDownload):
        observacao = valorNota = cnpj = tomador = cnae = valorNota = numeroNota = '-'
        cnpjBase = valorReceber = None

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

        if('Documento Auxiliar da NFS-e' in conteudo):
            observacao = ''
            valido = 'Sim'
            observadorClausula = observadorPeriodo = observadorConta = 0
            conteudo = re.sub('\xa0', ' ', conteudo)
            conteudo = re.split('\n', conteudo)
            print(conteudo)

            for id_linha, linha in dadosBaseCadastro.items():
                if(int(id_linha) == idProfessor):
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
                        valido = 'Não'
                        tomador = '-'
                        observacao = observacao + 'NFS-e sem tomador ou tomador incorreto. '
                        
                if('TOMADOR DO SERVIÇO NÃO IDENTIFICADO NA NFS-e' in linha):
                    tomador = '-'
                    valido = 'Não'
                    observacao = observacao + 'NFS-e sem tomador ou tomador incorreto. '

                if('Código de Tributação Nacional' in linha):
                    cnae = conteudo[i+1]
                    cnae = re.split(' - ', cnae)[0]
                    if(cnae != '08.02.01'):
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
                        observacao = observacao + 'Sem valor a receber informado na planilha Cadastro. '
                    valorNota = valorNota.replace('.', ',')

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
                valido = 'Não'
                observacao = observacao + 'Verificar CNPJ na NFS-e. '

            if(observadorClausula == 0):
                valido = 'Não'
                observacao = observacao + 'Verificar a referência a cláusula do contrato na descrição da NFSE. '
            
            if(observadorPeriodo == 0):
                valido = 'Não'
                observacao = observacao + 'Verificar o período de realização na descrição da NFS-e.'

            if(observadorConta == 0):
                valido = 'Não'
                observacao = observacao + 'Verificar a agência e conta na descrição da NFS-e.'

            novoNome = f"01-NFSE {nomeProfessor}.pdf"
            novoNome, duplicado = renomearArquivoDrive(service_drive, os.path.splitext(arquivo)[0], novoNome, idPasta)
            
            if duplicado:
                observacao += 'Existem arquivos de NFSE duplicados. '

            lancamentoControle(idProfessor, 'L', valido, observacao, valorNota, numeroNota, cliente_gspread, planilhaID)