import re
import os
from datetime import datetime
from MunicipiosPR.Excel.ExcelCertidoes import criarExcel, incluirNoExcel, fecharExcel
from MunicipiosPR.Interacoes.identificacao import identificacao

def verificarInvalidos(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha):
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
            if not(re.search('01-NFSE', arquivo)
            or re.search('02-CNDU', arquivo)
            or re.search('03-CNDT', arquivo)
            or re.search('04-CRF', arquivo) 
            or re.search('05-CNDE', arquivo)
            or re.search('06-CNDM', arquivo)
            or re.search('07-Relatório', arquivo)
            or re.search('.ini', arquivo)):
                documentoAvaliado = (
                    datetime.strftime(data,'%d/%m/%Y'),
                    arquivo,
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