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