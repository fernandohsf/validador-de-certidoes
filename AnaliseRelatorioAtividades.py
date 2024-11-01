import re
import locale
import calendar
import fitz
from datetime import datetime
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from MunicipiosPR.Excel.ExcelAtividades import criarExcel, incluirNoExcel, fecharExcel
from MunicipiosPR.Interacoes.identificacao import identificacao
from MunicipiosPR.Interacoes.googleDrive import listarArquivosDrive, baixarArquivo, renomearArquivoDrive

def validarAtividades(service, diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBase):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    data = datetime.today()
    #criarExcel(f'{diretorioRelatorio}/{nomeRelatorio} - {data.strftime("%d-%m-%Y(%Hh %Mm %Ss)")}.xlsx', nomePlanilha)

    linhaExcel = 0
    pastas = listarArquivosDrive(service, diretorioAvaliacao)

    for pasta in pastas:
        id, nomeEmissor = identificacao(pasta['name'])
        idPasta = pasta['id']
        arquivos = listarArquivosDrive(service, idPasta)

        for arquivo in arquivos:
            periodo = apto = cnpj = dataAssinatura = numeroNota = dataModificacao = valido = '-'
            observacao = ''
            cnpjBase = finalMesAnterior = None
            observador = 0
            apto = 'Apto'

            if not (arquivo['name'].endswith('.pdf') or arquivo['name'].endswith('.PDF')):
                continue

            caminhoPdfTemporario = f'G:\\Drives compartilhados\\PROJETOS\\Contratos\\01.CONVENIAR\\21 - Automação de análise jurídica\\Analisador de documentos\\tmp\\{arquivo["name"]}'
            baixarArquivo(service, arquivo['id'], caminhoPdfTemporario)

            try:
                pdf = fitz.open(caminhoPdfTemporario)
                conteudo = ''
                for page in pdf:
                    conteudo += page.get_text()
                pdf.close()
            except:
                continue

            if('RELATÓRIO DE PRESTAÇÃO DE SERVIÇOS' in conteudo or 'ELATÓRIO DE PRESTAÇÃO DE SERVIÇOS' in conteudo):    
            
                conteudo = re.sub('\xa0', ' ', conteudo)
                conteudo = re.split('\n', conteudo)
                
                valido = 'Sim'

                for id_linha, linha in dadosBase.items():
                    if(int(id_linha) == id):
                        cnpjBase = linha.get('CNPJ')
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
                        mesAnterior = datetime(ano, mes, 1)
                        finalMesAnterior = datetime(ano, mes, calendar.monthrange(ano, mes)[1])

                        if(mesAnterior.strftime('%BDE%Y').upper() in periodo
                        or mesAnterior.strftime('%B%Y').upper() in periodo
                        or f'{mesAnterior.strftime("%d/%m/%Y")}A{finalMesAnterior.strftime("%d/%m/%Y")}' in periodo
                        or f'{mesAnterior.strftime("%d/%m/%Y")}À{finalMesAnterior.strftime("%d/%m/%Y")}' in periodo
                        or f'{mesAnterior.strftime("%d/%m/%Y")}Á{finalMesAnterior.strftime("%d/%m/%Y")}' in periodo
                        or f'{mesAnterior.strftime("%d/%m/%Y")}ATÉ{finalMesAnterior.strftime("%d/%m/%Y")}' in periodo
                        or f'{mesAnterior.strftime("%d/%m")}A{finalMesAnterior.strftime("%d/%mDE%Y")}' in periodo):
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
                        dataAssinatura = linha.replace('.', '').replace('_', '').split(',')[-1].strip().upper()

                        try:
                            dataAssinatura = datetime.strptime(dataAssinatura, '%d DE %B DE %Y')
                            if(dataAssinatura < finalMesAnterior):
                                apto = 'Inapto'
                                valido = 'Não'
                                observacao = observacao + 'Verificar data de assinatura no relatório de atividades. '
                            dataAssinatura = dataAssinatura.strftime('%d de %B de %Y')
                        except:
                            apto = 'Inapto'
                            valido = 'Não'
                            observacao = observacao + 'Verificar data de assinatura no relatório de atividades. '
                    
                    if('N.º' in linha or 'Nº' in linha or 'N°' in linha or 'N.o' in linha):
                        try:
                            numeroNota = linha.split(':')[1].strip()
                            numeroNota = re.search(r'\d+', numeroNota).group()
                            if(len(numeroNota) == 50):
                                numeroNota = numeroNota[24:36]
                            numeroNota = int(numeroNota)
                        except:
                            apto = 'Inapto'
                            valido = 'Não'
                            observacao = observacao + 'Verificar o número da nota no relatório de atividades. '    
            
                if(observador == 0):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Verificar data de realização no relatório de atividades. '

                if(cnpj != cnpjBase):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Verificar CNPJ no relatório de atividades. '
                
                if(dataAssinatura == '-'):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Verificar data de assinatura no relatório de atividades. '

                if(numeroNota == '-'):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Verificar o número da nota no relatório de atividades. '

                dataModificacao = datetime.strptime(arquivo['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
                dataModificacao = dataModificacao.strftime('%d/%m/%Y')

                novoNome = f"07-Relatório {nomeEmissor}.pdf"
                nomeDocumento, duplicado = renomearArquivoDrive(service, arquivo['id'], novoNome, pasta['id'])
                
                if duplicado:
                    observacao += 'Existem arquivos de relatório de atividades duplicados. '
                
                documentoAvaliado = (
                    datetime.strftime(data,'%d/%m/%Y'),
                    nomeDocumento,
                    dataModificacao,
                    id,
                    nomeEmissor,
                    cnpj,
                    periodo,
                    dataAssinatura,
                    numeroNota,
                    apto,
                    observacao
                )
                linhaExcel +=1
                #incluirNoExcel(linhaExcel, 0, documentoAvaliado)

                lancamentoControle(id, 'M', valido, observacao, '', numeroNota)

    #fecharExcel()