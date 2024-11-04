from datetime import date
import os
import sys
from AnaliseNfse import validarNFSE
from AnaliseCNDU_Pj import validarCNDU
from AnaliseCNDT_Pj import validarCNDT
from AnaliseCRF_Pj import validarCRF
from AnaliseCNDE_PR_Pj import validarCNDE_PR
from AnaliseCNDM_PR import validarMunicipiosPR
from AnaliseRelatorioAtividades import validarAtividades
from MunicipiosPR.Interacoes.googleDrive import autenticarGoogleAPI, listarArquivosDrive
from MunicipiosPR.Interacoes.identificacao import identificacao

def atualizarBase(planilhaID, cliente_gspread):
    try:
        planilha_cadastro = cliente_gspread.open_by_key(planilhaID).worksheet('Cadastro')
        linhas_cadastro = planilha_cadastro.get_all_values()
        
        # Acessa a planilha Análise
        planilha_analise = cliente_gspread.open_by_key(planilhaID).worksheet('Disponível para Análise')
        linhas_analise = planilha_analise.get_all_values()

    except Exception as e:
        print(f"Erro ao acessar as planilhas: {e}")
        return {}, {}

    # Processa dados da planilha Cadastro
    cabecalho_cadastro = linhas_cadastro[0]
    colunasExtraidasCadastro = ['ID', 'Nome', 'CNPJ', 'Valor a receber']
    indicesColunasCadastro = [cabecalho_cadastro.index(coluna) for coluna in colunasExtraidasCadastro]

    dadosBaseCadastro = {
        linha[indicesColunasCadastro[0]]: {
            colunasExtraidasCadastro[i]: linha[indicesColunasCadastro[i]] for i in range(1, len(colunasExtraidasCadastro))
        }
        for linha in linhas_cadastro[1:]
    }

    # Processa dados da planilha Disponível para Análise
    cabecalho_analise = linhas_analise[0]
    colunasExtraidasAnalise = ['ID', 'Documentos estão aptos para seguir para pagamento?']
    indicesColunasAnalise = [cabecalho_analise.index(coluna) for coluna in colunasExtraidasAnalise]

    dadosBaseAnalise = {
        linha[indicesColunasAnalise[0]]: {
            colunasExtraidasAnalise[i]: linha[indicesColunasAnalise[i]] for i in range(1, len(colunasExtraidasAnalise))
        }
        for linha in linhas_analise[1:]
    }
    
    return dadosBaseCadastro, dadosBaseAnalise

def buscarPasta(service, nomePasta, idPastaPai=None):
    query = f"name = '{nomePasta}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if idPastaPai:
        query += f" and '{idPastaPai}' in parents"

    resultados = service.files().list(q=query, fields="files(id, name)").execute()
    arquivos = resultados.get('files', [])
    
    if arquivos:
        return arquivos[0]['id']  # Retorna o ID da primeira pasta encontrada
    return None

def BuscarPastaMesAnterior(service, idDiretorioBase):
    anoVigente = date.today().year
    mesAnterior = date.today().month-1
    anoAbreviado = date.today().strftime('%y')
    mes = ['Dez', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov']

    # Buscar a pasta do ano corrente ou anterior (caso o mês seja janeiro)
    pastaAnual = anoVigente if mesAnterior != 0 else anoVigente - 1
    idPastaAnual = buscarPasta(service, str(pastaAnual), idPastaPai=idDiretorioBase)
    if not idPastaAnual:
        print(f"Pasta do ano {pastaAnual} não encontrada.")
        return None
    
    idPastaAnalise = buscarPasta(service, 'Análise de Documentos' ,idPastaPai=idPastaAnual)
    if not idPastaAnalise:
        print("Pasta 'Análise de Documentos' não encontrada.")
        return None
    
    idPastaEmail = buscarPasta(service, 'e-Mail', idPastaPai=idPastaAnalise)
    if not idPastaEmail:
        print("Pasta 'e-Mail' não encontrada.")
        return None    
    
    for mesPasta in mes:
        if mesAnterior == 0:
            nome_pasta = f'{mesPasta}/{int(anoAbreviado) - 1}'
            break
        if mesAnterior == mes.index(mesPasta):
            nome_pasta = f'{mesPasta}/{anoAbreviado}'
            break
    
    idPastaMesAnterior = buscarPasta(service, nome_pasta, idPastaPai=idPastaEmail)
    
    return idPastaMesAnterior

#planilhaID = '1L_GtpCUd3_2uNGj8l64s7zr41ajyBUxxtxtVhQ5inLk' # Produção
#diretorioBaseDrive = '1ZinjciG-RUIi_cZxZzi2k-4YaNgm1Gft' # Produção
planilhaID = '1GSSDC9MOqEp3AuQJGe1DD9vV9Crdk7vHQGX9jhlPjOk' # Homologação
diretorioBaseDrive = '1yq5i3L1tHrztWPTiSVrwYKSFgpEy9DDl' # Homologação

service_drive, cliente_gspread = autenticarGoogleAPI()
dadosBaseCadastro, dadosBaseAnalise = atualizarBase(planilhaID, cliente_gspread)

idPastaMesAnterior = BuscarPastaMesAnterior(service_drive, diretorioBaseDrive)
pastas = listarArquivosDrive(service_drive, idPastaMesAnterior)

for pasta in pastas:
    downloadsTemp = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'Downloads')
    os.makedirs(downloadsTemp, exist_ok=True)

    id, nomeProfessor = identificacao(pasta['name'])
    idPastaProfessor = pasta['id']
    if str(id) in dadosBaseAnalise:
        status = dadosBaseAnalise[str(id)].get("Documentos estão aptos para seguir para pagamento?", "Status não encontrado")
        if status == 'Apto' or status == 'Inapto':
            continue

    print('Iniciando verificação de NFSE (Nota fiscal de serviço eletrônica). \nAguarde...')
    validarNFSE(service_drive, cliente_gspread, idPastaProfessor, dadosBaseCadastro, nomeProfessor, planilhaID)

    print('Verificação de NFSE finalizada. \nIniciando verficação de CNDU (Certidão negativa de débitos da União). \nAguarde...')
    validarCNDU(service_drive, idPastaMesAnterior, dadosBaseAnalise)  

    print('Verificação de CNDU finalizada. \nIniciando verificação de CNDT (Certidão negativa de débitos trabalhistas). \nAguarde...')
    validarCNDT(service_drive, idPastaMesAnterior, dadosBaseAnalise)  

    print('Verificação de CNDT finalizada. \nIniciando verificação de CRF (Certidão de regularidade do FGTS). \nAguarde...')
    validarCRF(service_drive, idPastaMesAnterior, dadosBaseAnalise)

    print('Verficação de CRF finalizada. \nIninciando verificação de CNDE (Certidão negativa de débitos estaduais). \nAguarde...')
    validarCNDE_PR(service_drive, idPastaMesAnterior, dadosBaseAnalise) 

    print('Verificação de CNDE finalizada. \nIniciando verificação de CNDM (Certidão negativa de débitos municipais). \nAguarde...')
    validarMunicipiosPR(service_drive, idPastaMesAnterior, dadosBaseAnalise)

    print('Verificação de CNDM finalizada. \nIniciando verificação de relatórios de atividades. \nAguarde...')
    validarAtividades(service_drive, idPastaMesAnterior, dadosBaseCadastro, dadosBaseAnalise)

    print('Verificação de relatórios de atividades finalizada.\nRelatório finalizado.\nFim da execução.')

#input('Pessione enter para encerrar...')