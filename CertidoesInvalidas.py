import re
from datetime import datetime
from MunicipiosPR.Excel.ExcelCertidoes import criarExcel, incluirNoExcel, fecharExcel
from MunicipiosPR.Interacoes.identificacao import identificacao
from MunicipiosPR.Interacoes.googleDrive import listarArquivosDrive

def verificarInvalidos(service, diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha):
    data = datetime.today()
    diretorioRelatorio = diretorioRelatorio
    nomeRelatorio = nomeRelatorio
    nomePlanilha = nomePlanilha
    criarExcel(f'{diretorioRelatorio}/{nomeRelatorio} - {data.strftime("%d-%m-%Y(%Hh %Mm %Ss)")}.xlsx', nomePlanilha)

    linhaExcel = 0
    pastas = listarArquivosDrive(service, diretorioAvaliacao)

    for pasta in pastas:
        id, nomeEmissor = identificacao(pasta['name'])
        idPasta = pasta['id']
        arquivos = listarArquivosDrive(service, idPasta)

        for arquivo in arquivos:  
            if not(re.search('01-NFSE', arquivo['name'])
            or re.search('02-CNDU', arquivo['name'])
            or re.search('03-CNDT', arquivo['name'])
            or re.search('04-CRF', arquivo['name']) 
            or re.search('05-CNDE', arquivo['name'])
            or re.search('06-CNDM', arquivo['name'])
            or re.search('07-Relatório', arquivo['name'])
            or re.search('.ini', arquivo['name'])):
                documentoAvaliado = (
                    datetime.strftime(data,'%d/%m/%Y'),
                    arquivo['name'],
                    '-',
                    id,
                    nomeEmissor,
                    '-',
                    '-',
                    '-',
                    '-',
                    '-',
                    'Não foi possível analisar o documento.'
                )

                linhaExcel +=1
                incluirNoExcel(linhaExcel, 0, documentoAvaliado)      
    
    fecharExcel()