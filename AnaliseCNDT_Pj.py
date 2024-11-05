import re
import fitz
from datetime import datetime
from MunicipiosPR.Interacoes.validade import verificarDataValidade
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from MunicipiosPR.Interacoes.identificacao import identificacao
from googleDrive import listarArquivosDrive, baixarArquivo, renomearArquivoDrive

def validarCNDT(service, diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseAnalise):
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
            apto = cnpj = dataValidade = diasValidade = codigoValidacao = dataModificacao = observacao = '-'

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

            if('CERTIDÃO NEGATIVA DE DÉBITOS TRABALHISTAS' in conteudo):
                apto = 'Apto'
                valido = 'Sim'
                observacao = ''
                conteudo = re.sub('\xa0', ' ', conteudo)
                conteudo = re.split('\n', conteudo)

                for linha in conteudo:
                    if('CNPJ:' in linha or 'CPF:' in linha):
                        cnpj = linha.split(': ')[-1].strip()

                    if('Validade:' in linha):
                        dataValidade = linha.split(': ')[-1].strip().split(' - ')[0].strip()
                        dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

                    if('Certidão nº:' in linha or 'Certidão n2:' in linha):
                        codigoValidacao = linha.split(': ')[-1].strip()
                
                try:
                    diasValidade, dataValidade, apto, valido = verificarDataValidade(data, dataValidade, apto, valido)
                    if(valido == 'Não'):
                        observacao += 'Verificar validade da Certidão CNDT. '
                except:
                    continue

                if(len(cnpj) != 18):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Certidão CNDT não é jurídica ou CNPJ inválido. '

                dataModificacao = datetime.strptime(arquivo['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
                dataModificacao = dataModificacao.strftime('%d/%m/%Y')

                novoNome = f"03-CNDT {nomeEmissor}.pdf"
                nomeDocumento, duplicado = renomearArquivoDrive(service, arquivo['id'], novoNome, pasta['id'])
                
                if duplicado:
                    observacao += 'Existem arquivos de CNDT duplicados. '
                
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

                lancamentoControle(id, 'J', valido, observacao, '', '')

    #fecharExcel()