import os
import re
import fitz
import calendar
from datetime import datetime
from integration.excel_drive import lancamento_controle
from integration.google_drive import renomear_arquivo_drive

def validar_NFSE(service_drive, cliente_gspread, dados_base_cadastro, pasta_download, id_pasta, id_professor, nome_professor, planilha_ID):
    data = datetime.today()

    for arquivo in os.listdir(pasta_download):
        observacao = valor_nota = cnpj = tomador = cnae = valor_nota = numero_nota = '-'
        cnpj_base = valor_receber = None

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

        if('Documento Auxiliar da NFS-e' in conteudo):
            observacao = ''
            valido = 'Sim'
            observador_clausula = observador_periodo = observador_conta = 0

            novo_nome = f"01-NFSE {nome_professor}.pdf"
            novo_nome, duplicado = renomear_arquivo_drive(service_drive, os.path.splitext(arquivo)[0], novo_nome, id_pasta)
            if duplicado:
                observacao += 'Existem arquivos de NFSE duplicados. '
                lancamento_controle(id_professor, 'L', '', observacao, '', '', cliente_gspread, planilha_ID)
                continue

            conteudo = re.sub('\xa0', ' ', conteudo)
            conteudo = re.split('\n', conteudo)

            for id_linha, linha in dados_base_cadastro.items():
                if(int(id_linha) == id_professor):
                    cnpj_base = linha.get('CNPJ')
                    valor_receber = linha.get('Valor a receber')
                    break
            
            for i, linha in enumerate(conteudo):
                if ('Chave de Acesso da NFS-e' in linha):
                    chave_acesso = conteudo[i+1].strip()
                    if(len(chave_acesso) != 50):
                        chave_acesso = conteudo[i+3].strip()

                if('Número da NFS-e' in linha):
                    numero_nota = conteudo[i+1]   

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
                    valor_nota = conteudo[i+1].split(' ')[-1].replace('.', '').replace(',', '.').strip()
                    if(valor_receber is not None):
                        valor_receber = valor_receber.replace('.', '').replace(',', '.').strip()
                        if(float(valor_nota) != float(valor_receber)):
                            valido = 'Não'
                            observacao = observacao + 'O valor total da nota difere do valor cadastrado. '
                    else:
                        observacao = observacao + 'Sem valor a receber informado na planilha Cadastro. '
                    valor_nota = valor_nota.replace('.', ',')

                if('ATIVIDADES DESCRITAS NA CLÁUSULA PRIMEIRA D' in linha.upper() 
                    or 'ATIVIDADES DESCRITAS NA CLAUSULA PRIMEIRA D' in linha.upper()
                    or 'ATIVIDADES DESCRITAS NA CLÁUSULA\nPRIMEIRA DO CONTRATO' in linha.upper()
                    or 'ATIVIDADES DESCRITAS NA CLÁUSULA 1º' in linha.upper()
                    or 'ATIVIDADES DESCRITAS NA CLAUSULA 1º' in linha.upper()
                    or 'DESCRITAS NA CLÁUSULA PRIMEIRA DO CONTRATO' in linha.upper()
                    or 'DESCRITAS NA CLAUSULA PRIMEIRA DO CONTRATO' in linha.upper()
                    or 'DESCRITO NA CLAUSULA PRIMEIRA DO CONTRATO' in linha.upper()):
                    observador_clausula += 1

                if('PERÍODO DE REALIZAÇÃO' in linha.upper()
                    or 'PERIODO DE REALIZAÇÃO' in linha.upper()
                    or 'PERIODO D REALIZAÇÃO' in linha.upper()
                    or 'COMPETÊNCIA:' in linha.upper()
                    or 'COMPETENCIA:' in linha.upper()):
                    linha = linha.upper()
                    periodo = linha.split('AÇÃO: ')[-1].split('.')[0].split(',')[0]
                    periodo = periodo.replace(' ', '')
                    mes = data.month - 1
                    ano = data.year

                    if(mes == 0):
                        mes = 12
                        ano -=1
                    mes_anterior = datetime(ano, mes, 1)
                    final_mes_anterior = datetime(ano, mes, calendar.monthrange(ano, mes)[1])

                    if(mes_anterior.strftime('%BDE%Y').upper() in periodo
                    or mes_anterior.strftime('%B%Y').upper() in periodo
                    or f'{mes_anterior.strftime("%d/%m/%Y")}A{final_mes_anterior.strftime("%d/%m/%Y")}' in periodo
                    or f'{mes_anterior.strftime("%d/%m/%Y")}À{final_mes_anterior.strftime("%d/%m/%Y")}' in periodo
                    or f'{mes_anterior.strftime("%d/%m/%Y")}Á{final_mes_anterior.strftime("%d/%m/%Y")}' in periodo
                    or f'{mes_anterior.strftime("%d/%m/%Y")}ATÉ{final_mes_anterior.strftime("%d/%m/%Y")}' in periodo
                    or f'{mes_anterior.strftime("%d/%m")}A{final_mes_anterior.strftime("%d/%mDE%Y")}' in periodo):
                        observador_periodo += 1

                if('AGÊNCIA' in linha.upper() or 'AGENCIA' in linha.upper() or 'AG:' in linha.upper()):
                    conta = conteudo[i:i+3]
                    for linha2 in conta:
                        if('CONTA' in linha2.upper()):
                            observador_conta += 1 

            if(cnpj == ''):
                observacao = observacao + 'Verificar CNPJ na NFS-e. '

            if(cnpj != cnpj_base):
                valido = 'Não'
                observacao = observacao + 'Verificar CNPJ na NFS-e. '

            if(observador_clausula == 0):
                valido = 'Não'
                observacao = observacao + 'Verificar a referência a cláusula do contrato na descrição da NFSE. '
            
            if(observador_periodo == 0):
                valido = 'Não'
                observacao = observacao + 'Verificar o período de realização na descrição da NFS-e.'

            if(observador_conta == 0):
                valido = 'Não'
                observacao = observacao + 'Verificar a agência e conta na descrição da NFS-e.'

            lancamento_controle(id_professor, 'L', valido, observacao, valor_nota, numero_nota, cliente_gspread, planilha_ID)