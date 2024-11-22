import os
import fitz
from datetime import datetime
from Utils import verificar_data_validade
from integration.excel_drive import lancamento_controle
from integration.google_drive import renomear_arquivo_drive

def importar_funcoes(modulos, prefixo):
    funcoes = {}

    for modulo in modulos:
        try:
            modulo_importado = __import__(modulo, fromlist=['']) 
            funcoes_modulo = {nome: getattr(modulo_importado, nome) for nome in dir(modulo_importado) if nome.startswith(prefixo) and callable(getattr(modulo_importado, nome))}
            funcoes.update(funcoes_modulo)
        except ImportError as e:
            print(f"Erro ao importar módulo {modulo}: {e}")
    return funcoes

def validar_Municipios_PR(service_drive, cliente_gspread, pasta_download, id_pasta, id_professor, nome_professor, planilha_ID):
    data = datetime.today()

    ### IMPORTANDO AS FUNÇÕES DOS MUNICIPIOS DO PARANÁ
    modulos = [
        'factory.AnaliseAlmiranteTamandare',
	    'factory.AnaliseAndira',
	    'factory.AnaliseApucarana',
        'factory.AnaliseArapongas',
        'factory.AnaliseArapoti',
	    'factory.AnaliseBarbosaFerraz',
	    'factory.AnaliseBelaVistaDoParaiso',
        'factory.AnaliseBoaVenturaDeSaoRoque',
        'factory.AnaliseBorrazopolis',
        'factory.AnaliseCampinaGrandeDoSul',
	    'factory.AnaliseCampoDoTenente',
        'factory.AnaliseCampoLargo',
        'factory.AnaliseCampoMourao',
        'factory.AnaliseCascavel',
        'factory.AnaliseChopinzinho',
        'factory.AnaliseClevelandia',
        'factory.AnaliseColorado',
        'factory.AnaliseCruzeiroDoOeste',
	    'factory.AnaliseDoisVizinhos',
	    'factory.AnaliseDoutorCamargo',
	    'factory.AnaliseFigueira',
	    'factory.AnaliseFranciscoBeltrao',
        'factory.AnaliseGoioere',
        'factory.AnaliseGuaira',
	    'factory.AnaliseGuaraci',
        'factory.AnaliseGuarapuava',
        'factory.AnaliseIbaiti',
        'factory.AnaliseIbipora',
        'factory.AnaliseImbau',
	    'factory.AnaliseIretama',
	    'factory.AnaliseItambe',
        'factory.AnaliseItapejaraDoeste',
        'factory.AnaliseIvaipora',
	    'factory.AnaliseIzabelDoOeste',
        'factory.AnaliseJaniopolis',
        'factory.AnaliseJapura',
	    'factory.AnaliseJardimAlegre',
        'factory.AnaliseJoaquimTavora',
	    'factory.AnaliseJussara',
	    'factory.AnaliseLapa',
        'factory.AnaliseLaranjeirasDoSul',
        'factory.AnaliseLondrina',
	    'factory.AnaliseLuiziana',
        'factory.AnaliseLunardelli',
	    'factory.AnaliseMandaguaçu',
        'factory.AnaliseMandaguari',
	    'factory.AnaliseMandirituba',
        'factory.AnaliseMarechalCandidoRondon',
        'factory.AnaliseMarilandiaDoSul',
        'factory.AnaliseMariluz',
        'factory.AnaliseMaringa',
	    'factory.AnaliseMarquinho',
        'factory.AnaliseMatinhos',
	    'factory.AnaliseNovaLondrina',
	    'factory.AnaliseNovaOlimpia',
        'factory.AnaliseNovasLaranjeiras',
        'factory.AnaliseOuroVerdeDoOeste',
        'factory.AnalisePalmital',
        'factory.AnaliseParaisoDoNorte',
        'factory.AnaliseParanagua',
	    'factory.AnalisePauloFrontin',
        'factory.AnalisePeabiru',
        'factory.AnalisePerobal',
        'factory.AnalisePiraiDoSul',
        'factory.AnalisePlanalto',
        'factory.AnalisePontaGrossa',
        'factory.AnaliseRibeiraoClaro',
	    'factory.AnaliseRibeiraoDoPinhal',
        'factory.AnaliseRioAzul',
        'factory.AnaliseSantaFe',
        'factory.AnaliseSantaHelena',
        'factory.AnaliseSantaIsabelDoIvai',
        'factory.AnaliseSantoAntonioDoSudoeste',
        'factory.AnaliseSaoJoaoDoIvai',
        'factory.AnaliseSaoJoseDosPinhais',
	    'factory.AnaliseSaoManoel',
	    'factory.AnaliseSiqueiraCampos',
	    'factory.AnaliseTerraBoa',
        'factory.AnaliseToledo',
	    'factory.AnaliseUniaoDaVitoria',
	    'factory.AnaliseVirmond',
	    'factory.AnaliseVitorino'
    ]
    funcoes = importar_funcoes(modulos, 'validar')

    for arquivo in os.listdir(pasta_download):
        cnpj = data_validade = observacao = valido = '-' 

        try:
            pdf = fitz.open(os.path.join(pasta_download, arquivo))
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
        for nome_funcao, funcao in funcoes.items():
            cnpj, data_validade = funcao(conteudo)
            if(cnpj == '-' or data_validade == '-'):
                continue

            novo_nome = f"06-CNDM {nome_professor}.pdf"
            novo_nome, duplicado = renomear_arquivo_drive(service_drive, os.path.splitext(arquivo)[0], novo_nome, id_pasta)
            if duplicado:
                observacao += 'Existem arquivos de CNDM duplicados. '
                lancamento_controle(id_professor, 'H', '', observacao, '', '', cliente_gspread, planilha_ID)
                continue

            try:
                valido = verificar_data_validade(data, data_validade, valido)
                if(valido == 'Não'):
                    observacao += 'Verificar validade da Certidão CNDM. '
            except:
                continue

            if(len(cnpj) != 18):
                valido = 'Não'
                observacao = observacao + 'Certidão CNDM não é jurídica ou CNPJ inválido. '

            lancamento_controle(id_professor, 'H', valido, observacao, '', '', cliente_gspread, planilha_ID)