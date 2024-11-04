import os
import sys
from datetime import date
from AnaliseNfse import validarNFSE
from AnaliseCNDU_Pj import validarCNDU
from AnaliseCNDT_Pj import validarCNDT
from AnaliseCRF_Pj import validarCRF
from AnaliseCNDE_PR_Pj import validarCNDE_PR
from AnaliseCNDM_PR import validarMunicipiosPR
from AnaliseRelatorioAtividades import validarAtividades
from CertidoesInvalidas import verificarInvalidos
from MunicipiosPR.Interacoes.googleDrive import autenticarGoogleAPI

def atualizarBase():
    #planilhaID = '1L_GtpCUd3_2uNGj8l64s7zr41ajyBUxxtxtVhQ5inLk' # Produção
    planilhaID = '1GSSDC9MOqEp3AuQJGe1DD9vV9Crdk7vHQGX9jhlPjOk' # Homologação

    try:
        service_drive, cliente_gspread = autenticarGoogleAPI()
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

    # Processa dados da planilha Análise
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
            nome_pasta = f'{mesPasta} {int(anoAbreviado) - 1}'
            break
        if mesAnterior == mes.index(mesPasta):
            nome_pasta = f'{mesPasta} {anoAbreviado}'
            break
    
    idPastaMesAnterior = buscarPasta(service, nome_pasta, idPastaPai=idPastaEmail)
    
    return idPastaMesAnterior

#diretorioBaseDrive = '1ZinjciG-RUIi_cZxZzi2k-4YaNgm1Gft' # Produção
diretorioBaseDrive = '1yq5i3L1tHrztWPTiSVrwYKSFgpEy9DDl' # Homologação
diretorioRelatorio = 'G:\\Drives compartilhados\\PROJETOS\\Contratos\\01.CONVENIAR\\21 - Automação de análise jurídica\\Relatórios de análise' #Produção
#diretorioRelatorio = 'D:\\Downloads' # Homologação

dadosBaseCadastro, dadosBaseAnalise = atualizarBase()
service_drive, cliente_gspread = autenticarGoogleAPI()
idPastaMesAnterior = BuscarPastaMesAnterior(service_drive, diretorioBaseDrive)

print('Iniciando verificação de NFSE (Nota fiscal de serviço eletrônica). \nAguarde...')
nomeRelatorio = 'Relatório de Validação NFSE'
nomePlanilha = 'NFSE'
status = validarNFSE(service_drive, idPastaMesAnterior, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseCadastro, dadosBaseAnalise)

print('Verificação de NFSE finalizada. \nIniciando verficação de CNDU (Certidão negativa de débitos da União). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CNDU'
nomePlanilha = 'CNDU'
validarCNDU(service_drive, idPastaMesAnterior, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseAnalise)  

print('Verificação de CNDU finalizada. \nIniciando verificação de CNDT (Certidão negativa de débitos trabalhistas). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CNDT'
nomePlanilha = 'CNDT'
validarCNDT(service_drive, idPastaMesAnterior, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseAnalise)  

print('Verificação de CNDT finalizada. \nIniciando verificação de CRF (Certidão de regularidade do FGTS). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CRF'
nomePlanilha = 'CRF'
validarCRF(service_drive, idPastaMesAnterior, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseAnalise)

### INÍCIO DAS VERIFICAÇÕES DO PARANÁ ###

print('Verficação de CRF finalizada. \nIninciando verificação de CNDE (Certidão negativa de débitos estaduais). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CNDE'
nomePlanilha = 'CNDE'
validarCNDE_PR(service_drive, idPastaMesAnterior, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseAnalise) 

print('Verificação de CNDE finalizada. \nIniciando verificação de CNDM (Certidão negativa de débitos municipais). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CNDM'
nomePlanilha = 'CNDM'
validarMunicipiosPR(service_drive, idPastaMesAnterior, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseAnalise)

### FIM DAS VERIFICAÇÕES DO PARANÁ ###

print('Verificação de CNDM finalizada. \nIniciando verificação de relatórios de atividades. \nAguarde...')
nomeRelatorio = 'Relatório de Validação de Atividades'
nomePlanilha = 'Atividades'
validarAtividades(service_drive, idPastaMesAnterior, diretorioRelatorio, nomeRelatorio, nomePlanilha, dadosBaseCadastro, dadosBaseAnalise)

print('Verificação de relatórios de atividades finalizada.')
#nomeRelatorio = 'Relatório de documento não avaliados'
#nomePlanilha = 'Não-lidos'
#verificarInvalidos(service_drive, idPastaMesAnterior, diretorioRelatorio, nomeRelatorio, nomePlanilha)

print('\nRelatório finalizado. \nFim da execução.')

#input('Pessione enter para encerrar...')