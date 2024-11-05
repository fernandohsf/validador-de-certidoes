import os
import fitz
from datetime import datetime
from MunicipiosPR.Interacoes.validade import verificarDataValidade
from MunicipiosPR.Excel.ExcelDrive import lancamentoControle
from googleDrive import renomearArquivoDrive

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

def validarMunicipiosPR(service_drive, cliente_gspread, pastaDownload, idPasta, idProfessor, nomeProfessor, planilhaID):
    print('Iniciando análise de CNDM (Certidão negativa de débitos Municipais). \nAguarde...')
    data = datetime.today()

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

    for arquivo in os.listdir(pastaDownload):
        cnpj = dataValidade = observacao = valido = '-' 

        try:
            pdf = fitz.open(os.path.join(pastaDownload, arquivo))
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

        valido = 'Sim'
        observacao = ''

        ### VALIDANDO O ARQUIVO EM CADA MUNICIPIO
        for nomeFuncao, funcao in funcoes.items():
            cnpj, dataValidade = funcao(conteudo)
            if(cnpj == '-' or dataValidade == '-'):
                continue

            novoNome = f"06-CNDM {nomeProfessor}.pdf"
            novoNome, duplicado = renomearArquivoDrive(service_drive, os.path.splitext(arquivo)[0], novoNome, idPasta)
            if duplicado:
                observacao += 'Existem arquivos de CNDM duplicados. '
                lancamentoControle(idProfessor, 'H', '', observacao, '', '', cliente_gspread, planilhaID)
                continue

            try:
                valido = verificarDataValidade(data, dataValidade, valido)
                if(valido == 'Não'):
                    observacao += 'Verificar validade da Certidão CNDM. '
            except:
                continue

            if(len(cnpj) != 18):
                valido = 'Não'
                observacao = observacao + 'Certidão CNDM não é jurídica ou CNPJ inválido. '

            lancamentoControle(idProfessor, 'H', valido, observacao, '', '', cliente_gspread, planilhaID)
    print('Análise concluída.')