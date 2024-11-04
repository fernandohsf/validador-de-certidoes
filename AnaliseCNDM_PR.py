import fitz
from datetime import datetime
from MunicipiosPR.Interacoes.validade import verificarDataValidade
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from MunicipiosPR.Interacoes.identificacao import identificacao
from MunicipiosPR.Interacoes.googleDrive import listarArquivosDrive, baixarArquivo, renomearArquivoDrive

def importarFuncoes(modulos, prefixo):
    funcoes = {}

    for modulo in modulos:
        try:
            moduloImportado = __import__(modulo, fromlist=['']) 
            funcoesModulo = {nome: getattr(moduloImportado, nome) for nome in dir(moduloImportado) if nome.startswith(prefixo) and callable(getattr(moduloImportado, nome))}
            funcoes.update(funcoesModulo)
        except ImportError as e:
            print(f"Erro ao importar módulo {modulo}: {e}")
    return funcoes

def validarMunicipiosPR(service, diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseAnalise):
    data = datetime.today()
    #criarExcel(f'{diretorioRelatorio}/{nomeRelatorio} - {data.strftime("%d-%m-%Y(%Hh %Mm %Ss)")}.xlsx', nomePlanilha)
    linhaExcel = 0

    ### IMPORTANDO AS FUNÇÕES DOS MUNICIPIOS DO PARANÁ
    modulos = [
        'MunicipiosPR.AnaliseAlmiranteTamandare',
	    'MunicipiosPR.AnaliseAndira',
	    'MunicipiosPR.AnaliseApucarana',
        'MunicipiosPR.AnaliseArapongas',
        'MunicipiosPR.AnaliseArapoti',
	    'MunicipiosPR.AnaliseBarbosaFerraz',
	    'MunicipiosPR.AnaliseBelaVistaDoParaiso',
        'MunicipiosPR.AnaliseBoaVenturaDeSaoRoque',
        'MunicipiosPR.AnaliseBorrazopolis',
        'MunicipiosPR.AnaliseCampinaGrandeDoSul',
	    'MunicipiosPR.AnaliseCampoDoTenente',
        'MunicipiosPR.AnaliseCampoLargo',
        'MunicipiosPR.AnaliseCampoMourao',
        'MunicipiosPR.AnaliseCascavel',
        'MunicipiosPR.AnaliseChopinzinho',
        'MunicipiosPR.AnaliseClevelandia',
        'MunicipiosPR.AnaliseColorado',
        'MunicipiosPR.AnaliseCruzeiroDoOeste',
	    'MunicipiosPR.AnaliseDoisVizinhos',
	    'MunicipiosPR.AnaliseDoutorCamargo',
	    'MunicipiosPR.AnaliseFigueira',
	    'MunicipiosPR.AnaliseFranciscoBeltrao',
        'MunicipiosPR.AnaliseGoioere',
        'MunicipiosPR.AnaliseGuaira',
	    'MunicipiosPR.AnaliseGuaraci',
        'MunicipiosPR.AnaliseGuarapuava',
        'MunicipiosPR.AnaliseIbaiti',
        'MunicipiosPR.AnaliseIbipora',
        'MunicipiosPR.AnaliseImbau',
	    'MunicipiosPR.AnaliseIretama',
	    'MunicipiosPR.AnaliseItambe',
        'MunicipiosPR.AnaliseItapejaraDoeste',
        'MunicipiosPR.AnaliseIvaipora',
	    'MunicipiosPR.AnaliseIzabelDoOeste',
        'MunicipiosPR.AnaliseJaniopolis',
        'MunicipiosPR.AnaliseJapura',
	    'MunicipiosPR.AnaliseJardimAlegre',
        'MunicipiosPR.AnaliseJoaquimTavora',
	    'MunicipiosPR.AnaliseJussara',
	    'MunicipiosPR.AnaliseLapa',
        'MunicipiosPR.AnaliseLaranjeirasDoSul',
        'MunicipiosPR.AnaliseLondrina',
	    'MunicipiosPR.AnaliseLuiziana',
        'MunicipiosPR.AnaliseLunardelli',
	    'MunicipiosPR.AnaliseMandaguaçu',
        'MunicipiosPR.AnaliseMandaguari',
	    'MunicipiosPR.AnaliseMandirituba',
        'MunicipiosPR.AnaliseMarechalCandidoRondon',
        'MunicipiosPR.AnaliseMarilandiaDoSul',
        'MunicipiosPR.AnaliseMariluz',
        'MunicipiosPR.AnaliseMaringa',
	    'MunicipiosPR.AnaliseMarquinho',
        'MunicipiosPR.AnaliseMatinhos',
	    'MunicipiosPR.AnaliseNovaLondrina',
	    'MunicipiosPR.AnaliseNovaOlimpia',
        'MunicipiosPR.AnaliseNovasLaranjeiras',
        'MunicipiosPR.AnaliseOuroVerdeDoOeste',
        'MunicipiosPR.AnalisePalmital',
        'MunicipiosPR.AnaliseParaisoDoNorte',
        'MunicipiosPR.AnaliseParanagua',
	    'MunicipiosPR.AnalisePauloFrontin',
        'MunicipiosPR.AnalisePeabiru',
        'MunicipiosPR.AnalisePerobal',
        'MunicipiosPR.AnalisePiraiDoSul',
        'MunicipiosPR.AnalisePlanalto',
        'MunicipiosPR.AnalisePontaGrossa',
        'MunicipiosPR.AnaliseRibeiraoClaro',
	    'MunicipiosPR.AnaliseRibeiraoDoPinhal',
        'MunicipiosPR.AnaliseRioAzul',
        'MunicipiosPR.AnaliseSantaFe',
        'MunicipiosPR.AnaliseSantaHelena',
        'MunicipiosPR.AnaliseSantaIsabelDoIvai',
        'MunicipiosPR.AnaliseSantoAntonioDoSudoeste',
        'MunicipiosPR.AnaliseSaoJoaoDoIvai',
        'MunicipiosPR.AnaliseSaoJoseDosPinhais',
	    'MunicipiosPR.AnaliseSaoManoel',
	    'MunicipiosPR.AnaliseSiqueiraCampos',
	    'MunicipiosPR.AnaliseTerraBoa',
        'MunicipiosPR.AnaliseToledo',
	    'MunicipiosPR.AnaliseUniaoDaVitoria',
	    'MunicipiosPR.AnaliseVirmond',
	    'MunicipiosPR.AnaliseVitorino'
    ]
    funcoes = importarFuncoes(modulos, 'validar')

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
            apto = cnpj = dataValidade = diasValidade = dataModificacao = observacao = valido = codigoValidacao = '-' 

            if not (arquivo['name'].endswith('.pdf') or arquivo['name'].endswith('.PDF')):
                continue

            caminhoPdfTemporario = f'G:\\Drives compartilhados\\PROJETOS\\Contratos\\01.CONVENIAR\\21 - Automação de análise jurídica\\Analisador de documentos\\tmp\\{arquivo["name"]}'
            baixarArquivo(service, arquivo['id'], caminhoPdfTemporario)

            try:
                pdf = fitz.open(caminhoPdfTemporario)
                conteudo = ''
                if pdf.page_count > 2:
                    continue
                for page in pdf:
                    conteudo += page.get_text()
                pdf.close()
            except:
                continue

            if (len(conteudo) < 200):
                continue
        
            apto =  'Apto'
            valido = 'Sim'
            observacao = ''

            ### VALIDANDO O ARQUIVO EM CADA MUNICIPIO
            for nomeFuncao, funcao in funcoes.items():

                cnpj, dataValidade = funcao(conteudo)

                if(cnpj == '-' or dataValidade == '-'):
                    continue

                try:
                    diasValidade, dataValidade, apto, valido = verificarDataValidade(data, dataValidade, apto, valido)
                    if(valido == 'Não'):
                        observacao += 'Verificar validade da Certidão CNDM. '
                except:
                    continue

                if(len(cnpj) != 18):
                    apto = 'Inapto'
                    valido = 'Não'
                    observacao = observacao + 'Certidão CNDM não é jurídica ou CNPJ inválido. '

                dataModificacao = datetime.strptime(arquivo['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
                dataModificacao = dataModificacao.strftime('%d/%m/%Y')

                novoNome = f"06-CNDM {nomeEmissor}.pdf"
                nomeDocumento, duplicado = renomearArquivoDrive(service, arquivo['id'], novoNome, pasta['id'])
                
                if duplicado:
                    observacao += 'Existem arquivos de CNDM duplicados. '
                    
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

                lancamentoControle(id, 'H', valido, observacao, '', '')

    #fecharExcel()