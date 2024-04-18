import re
import os
import shutil
import time
from tika import parser
from datetime import datetime
from pytesseract import pytesseract
from pdf2jpg import pdf2jpg
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from MunicipiosPR.Excel.ExcelCertidoes import criarExcel, incluirNoExcel, fecharExcel
from MunicipiosPR.Interacoes.identificacao import identificacao

def analiseImagens(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha):
    tesseract = 'C:/Users/fernando.ferreira/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
    pytesseract.tesseract_cmd = tesseract

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
            certidao = apto = cnpj = dataValidade = diasValidade = codigoValidacao = dataModificacao = observacao = img = '-'

            if arquivo.endswith('.pdf'):
                conteudo = parser.from_file(f'{pasta}/{arquivo}')

                if(conteudo['content'] is None or len(conteudo['content']) < 200):
                    pdf = os.path.join(pasta, arquivo)
                    imagem_dir = os.path.join(pasta, f'{arquivo}_dir')
                    pdf2jpg.convert_pdf2jpg(pdf, pasta)
                    img = os.path.join(imagem_dir, f'0_{arquivo}.jpg')
                else:
                    continue                
            else: 
                img = os.path.join(pasta, arquivo)
            try:
                texto = pytesseract.image_to_string(img)
            except:
                continue
           
            texto = re.split('\n', texto)

            if('Certificado de Regularidade' in texto
               or 'Certificado de Regularidade do FGTS - CRF' in texto):
                certidao = 'Regular'
                apto = 'Apto' 
                valido = 'Sim'
                observador = 0   

                for linha in texto:
                    if any(palavra in linha for palavra in 
                           ['Inscricao:', 
                            'Inscrig&o:', 
                            'Inscricgao:', 
                            'Inscrigado:', 
                            'Inscrigao:', 
                            'Inscrigaéo:', 
                            'Inscricgdo:', 
                            'Inscrigdo:', 
                            'Inscrig¢do:', 
                            'Inserigfo:', 
                            'Inscrigao:'
                            ]):
                        cnpj = linha.split()[-1]

                    if any(palavra in linha for palavra in 
                           ['encontra-se em situacao regular', 
                            'encontra-se em situacgdo regular', 
                            'encontra-se em situacdo regular', 
                            'encontra-se em situagao regular', 
                            'encontra-se em situacado regular', 
                            'encontra-se em situacado regular', 
                            'encontra-se em situagdo regular', 
                            'encontra-se em situagae regular', 
                            'encontra-se em situacgao regular', 
                            'encontra-se em situacéo regular', 
                            'encontra-se em situagde regular'
                            ]):
                        observador += 1

                    if any(palavra in linha for palavra in 
                           ['Numero:', 
                            'Ndmero:', 
                            'Nimero:', 
                            'NUmero:', 
                            'Nidmero:', 
                            'Namero:', 
                            'Naomero:', 
                            'NGmero:', 
                            'N&mero:'
                            ]):
                        codigoValidacao = linha.split()[-1]
                    
                    if any(palavra in linha for palavra in 
                           ['Validade', 
                            'jade:'
                            ]):
                        dataValidade = linha.split()[-1]
                        dataValidade = ''.join(re.findall(r'(\w+/\w+/\w+)', dataValidade))
                        dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                        if(dataValidade < data):
                            apto = 'Inapto'
                            valido = 'Não'
                            observacao = observacao + 'Certidão vencida '
                        diasValidade = dataValidade - data

                if(len(cnpj) > 18):
                    cnpj = re.split('—', cnpj)[-1]
                if(len(cnpj) != 18):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = 'Verificar CNPJ. '
                if(cnpj == '-'):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = 'Verificar CNPJ. '
                
                if(codigoValidacao == '-'):
                        apto = 'Inapto'
                        valido = 'Não'
                        observacao = observacao + 'Sem código de validação. '

                if(observador != 1):
                    certidao = 'Irregular'
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'CNPJ não está regular ao FGTS. '

                if arquivo.endswith('.pdf'):
                    nomeDocumento = f'05-CRF {nomeEmissor}.pdf'
                else:
                    nomeDocumento = f'05-CRF {nomeEmissor}.jpg'

                try:
                    os.rename(os.path.join(pasta, arquivo), os.path.join(pasta, nomeDocumento))
                except:
                    os.rename(os.path.join(pasta, arquivo), os.path.join(pasta, f'DUPLICADO {nomeDocumento}'))
                    observacao += 'Arquivo duplicado. '

                dataModificacao = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime(os.path.join(pasta, nomeDocumento))))   
                
                documentoAvaliado = (
                        datetime.strftime(data,'%d/%m/%Y'),
                        nomeDocumento,
                        dataModificacao,
                        id,
                        nomeEmissor,
                        cnpj,
                        certidao,
                        codigoValidacao,
                        datetime.strftime(dataValidade,'%d/%m/%Y'),
                        int(diasValidade.days),
                        apto,
                        observacao
                    )
                linhaExcel +=1
                incluirNoExcel(linhaExcel, 0, documentoAvaliado)

                lancamentoControle(id, 'K', valido, observacao ,'', '')

            try:
                shutil.rmtree(f'{pasta}/{arquivo}_dir')
            except:
                continue

    fecharExcel()