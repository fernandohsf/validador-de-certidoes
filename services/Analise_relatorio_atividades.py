import os
import re
import locale
import calendar
import fitz
from datetime import datetime
from integration.excel_drive import lancamento_controle
from integration.google_drive import renomear_arquivo_drive

def validar_atividades(service_drive, cliente_gspread, dados_base_cadastro, pasta_download, id_pasta, id_professor, nome_professor, planilha_ID):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    data = datetime.today()

    for arquivo in os.listdir(pasta_download):
        periodo = cnpj = data_assinatura = numero_nota = valido = '-'
        observacao = ''
        cnpj_base = final_mes_anterior = None
        observador = 0

        try:
            pdf = fitz.open(os.path.join(pasta_download, arquivo))
            conteudo = ''
            for page in pdf:
                conteudo += page.get_text()
            pdf.close()
        except:
            continue

        if('RELATÓRIO DE PRESTAÇÃO DE SERVIÇOS' in conteudo or 'ELATÓRIO DE PRESTAÇÃO DE SERVIÇOS' in conteudo):    

            novo_nome = f"07-RELATÓRIO {nome_professor}.pdf"
            novo_nome, duplicado = renomear_arquivo_drive(service_drive, os.path.splitext(arquivo)[0], novo_nome, id_pasta)
            if duplicado:
                observacao += 'Existem arquivos de relatório de atividades duplicados. '
                lancamento_controle(id_professor, 'M', '', observacao, '', '', cliente_gspread, planilha_ID)
                continue

            conteudo = re.sub('\xa0', ' ', conteudo)
            conteudo = re.split('\n', conteudo)
            valido = 'Sim'

            for id_linha, linha in dados_base_cadastro.items():
                if(int(id_linha) == id_professor):
                    cnpj_base = linha.get('CNPJ')
                    break

            for i, linha in enumerate(conteudo):
                if('CNPJ' in linha):
                    cnpj = linha.replace(' ', '').replace('.', '').replace('/', '').replace('-', '').replace('\\', '').replace('_', '').replace(':', '').replace('(', '').replace(')', '')
                    cnpj = cnpj.split('CNPJ')[-1][:14]
                    cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

                    if(cnpj == '../-'):
                        cnpj = conteudo[i+1]
                        cnpj = cnpj.replace(' ', '').replace('.', '').replace('/', '').replace('-', '').replace('\\', '').replace('_', '').replace(':', '').replace('(', '').replace(')', '')
                        cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
                    
                if('PERÍODO DE REALIZAÇÃO DAS AÇÕES' in linha or 'PERÍODO DE REALIZAÇÃO DAS ATIVIDADES' in linha):
                    periodo = linha.split(': ')[-1].upper()
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
                        observador +=1
                    
                if any(palavra in linha for palavra in 
                    [' PR,',
                        'Mourão,',
                        'aPR,',
                        '/PR,',
                        '-PR,',
                        'Imbaú,',
                        'Paraná,',
                        'Curitiba,',
                        'Guarapuava,',
                        'Ivaiporã,',
                        ]):
                    data_assinatura = linha.replace('.', '').replace('_', '').split(',')[-1].strip().upper()

                    try:
                        data_assinatura = datetime.strptime(data_assinatura, '%d DE %B DE %Y')
                        if(data_assinatura < final_mes_anterior):
                            valido = 'Não'
                            observacao = observacao + 'Verificar data de assinatura no relatório de atividades. '
                        data_assinatura = data_assinatura.strftime('%d de %B de %Y')
                    except:
                        valido = 'Não'
                        observacao = observacao + 'Verificar data de assinatura no relatório de atividades. '
                
                if('N.º' in linha or 'Nº' in linha or 'N°' in linha or 'N.o' in linha):
                    try:
                        numero_nota = linha.split(':')[1].strip()
                        numero_nota = re.search(r'\d+', numero_nota).group()
                        if(len(numero_nota) == 50):
                            numero_nota = numero_nota[24:36]
                        numero_nota = int(numero_nota)
                    except:
                        valido = 'Não'
                        observacao = observacao + 'Verificar o número da nota no relatório de atividades. '    
        
            if(observador == 0):
                valido = 'Não'
                observacao = observacao + 'Verificar data de realização no relatório de atividades. '

            if(cnpj != cnpj_base):
                valido = 'Não'
                observacao = observacao + 'Verificar CNPJ no relatório de atividades. '
            
            if(data_assinatura == '-'):
                valido = 'Não'
                observacao = observacao + 'Verificar data de assinatura no relatório de atividades. '

            if(numero_nota == '-'):
                valido = 'Não'
                observacao = observacao + 'Verificar o número da nota no relatório de atividades. '

            lancamento_controle(id_professor, 'M', valido, observacao, '', numero_nota, cliente_gspread, planilha_ID)