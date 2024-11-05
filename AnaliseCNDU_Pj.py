import re
import fitz
from datetime import datetime
from MunicipiosPR.Interacoes.validade import verificarDataValidade
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from googleDrive import listarArquivosDrive, baixarArquivo, renomearArquivoDrive

def validarCNDU(service, diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseAnalise):
    data = datetime.today()
    #criarExcel(f'{diretorioRelatorio}/{nomeRelatorio} - {data.strftime("%d-%m-%Y(%Hh %Mm %Ss)")}.xlsx', nomePlanilha)

    linhaExcel = 0
    pastas = listarArquivosDrive(service, diretorioAvaliacao)

    for pasta in pastas:
        id, nomeEmissor = identificacao(pasta['name'])
        idPasta = pasta['id']
        if str(id) in dadosBaseAnalise:
            status = dadosBaseAnalise[str(id)].get("Documentos estão aptos para seguir para pagamento?", "Status não encontrado")
            if status == 'Apto' or status == 'Inapto':
                continue
        arquivos = listarArquivosDrive(service, idPasta)

        for arquivo in arquivos:
            apto = cnpj = dataValidade = diasValidade = codigoValidacao = dataModificacao = observacao = valido = '-'

            if not (arquivo['name'].endswith('.pdf') or arquivo['name'].endswith('.PDF')):
                continue

            caminhoPdfTemporario = f'G:\\Drives compartilhados\\PROJETOS\\Contratos\\01.CONVENIAR\\21 - Automação de análise jurídica\\Analisador de documentos\\tmp\\{arquivo["name"]}'
            baixarArquivo(service, arquivo['id'], caminhoPdfTemporario)

            try:
                pdf = fitz.open(caminhoPdfTemporario)
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

            if('CERTIDÃO NEGATIVA DE DÉBITOS RELATIVOS AOS TRIBUTOS FEDERAIS' in conteudo 
            or 'CERTIDÃO POSITIVA COM EFEITOS DE NEGATIVA DE DÉBITOS RELATIVOS AOS TRIBUTOS\nFEDERAIS' in conteudo):
                apto = 'Apto'
                valido = 'Sim'
                observacao = ''
                conteudo = re.sub('\xa0', ' ', conteudo)
                conteudo = re.split('\n', conteudo)

                for linha in conteudo:
                    if('CNPJ:' in linha or 'CPF:' in linha):
                        cnpj = linha.split(': ')[-1].strip()
                        
                    if('Válida até' in linha):  
                        dataValidade = linha.strip().split(' ')[-1].replace('.', '')
                        dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

                    if('Código de controle' in linha):
                        codigoValidacao = linha.split(': ')[-1].strip()

                try:
                    diasValidade, dataValidade, apto, valido = verificarDataValidade(data, dataValidade, apto, valido)
                    if(valido == 'Não'):
                        observacao += 'Verificar validade da Certidão CNDU. '
                except:
                    continue

                if(len(cnpj) != 18):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Certidão CNDU não é jurídica ou CNPJ inválido. '

                nomeDocumento = f'02-CNDU {nomeEmissor}.pdf'

                dataModificacao = datetime.strptime(arquivo['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
                dataModificacao = dataModificacao.strftime('%d/%m/%Y')

                novoNome = f"02-CNDU {nomeEmissor}.pdf"
                nomeDocumento, duplicado = renomearArquivoDrive(service, arquivo['id'], novoNome, pasta['id'])
                
                if duplicado:
                    observacao += 'Existem arquivos de CNDU duplicados. '
                
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
                #incluirNoExcel(linhaExcel, 0, documentoAvaliado)

                lancamentoControle(id, 'I', valido, observacao, '', '')

    #fecharExcel()