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
import gspread
from google.oauth2.service_account import Credentials

def atualizarBase():
    caminhoBase = os.path.dirname(os.path.abspath(sys.argv[0]))
    caminho_credenciais = os.path.join(caminhoBase, 'credenciais_google.json')

    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(caminho_credenciais, scopes=scope)
    cliente = gspread.authorize(creds)

    planilhaID = '1L_GtpCUd3_2uNGj8l64s7zr41ajyBUxxtxtVhQ5inLk' # Produção
    #planilhaID = '1GSSDC9MOqEp3AuQJGe1DD9vV9Crdk7vHQGX9jhlPjOk' # Homologação
    planilha = cliente.open_by_key(planilhaID).worksheet('Cadastro')

    linhas = planilha.get_all_values()

    cabecalho = linhas[0]
    colunas_a_retirar = ['ID', 'Nome', 'CNPJ', 'Valor a receber']
    indices_colunas = [cabecalho.index(coluna) for coluna in colunas_a_retirar]

    dadosBase = {
        linha[indices_colunas[0]]: {
            colunas_a_retirar[i]: linha[indices_colunas[i]] for i in range(1, len(colunas_a_retirar))
        }
        for linha in linhas[1:]
    }

    return dadosBase

base = atualizarBase()

diretorioAvaliacao = 'G:\\Drives compartilhados\\PROJETOS\\Contratos\\01.CONVENIAR\\21 - Automação de análise jurídica\\Notas e certidões'
#diretorioAvaliacao = 'D:\\Downloads'
diretorioRelatorio = 'G:\\Drives compartilhados\\PROJETOS\\Contratos\\01.CONVENIAR\\21 - Automação de análise jurídica\\Relatórios de análise'
#diretorioRelatorio = 'D:\\Downloads'

mesAnterior = date.today().month-1
ano = date.today().strftime('%y')
mes = ['Dez','Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov']

for mesPasta in mes:
    if(mesAnterior == 0):
        diretorioAvaliacao = diretorioAvaliacao + f'/{mesPasta} {int(ano)-1}'
        break
    if(mesAnterior == mes.index(mesPasta)):
        diretorioAvaliacao = diretorioAvaliacao + f'/{mesPasta} {ano}'
        break

print('Iniciando verificação de NFSE (Nota fiscal de serviço eletrônica). \nAguarde...')
nomeRelatorio = 'Relatório de Validação NFSE'
nomePlanilha = 'NFSE'
validarNFSE(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha, base)

print('Verificação de NFSE finalizada. \nIniciando verficação de CNDU (Certidão negativa de débitos da União). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CNDU'
nomePlanilha = 'CNDU'
validarCNDU(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha)  

print('Verificação de CNDU finalizada. \nIniciando verificação de CNDT (Certidão negativa de débitos trabalhistas). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CNDT'
nomePlanilha = 'CNDT'
validarCNDT(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha)  

print('Verificação de CNDT finalizada. \nIniciando verificação de CRF (Certidão de regularidade do FGTS). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CRF'
nomePlanilha = 'CRF'
validarCRF(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha)

### INÍCIO DAS VERIFICAÇÕES DO PARANÁ ###

print('Verficação de CRF finalizada. \nIninciando verificação de CNDE (Certidão negativa de débitos estaduais). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CNDE'
nomePlanilha = 'CNDE'
validarCNDE_PR(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha) 

print('Verificação de CNDE finalizada. \nIniciando verificação de CNDM (Certidão negativa de débitos municipais). \nAguarde...')
nomeRelatorio = 'Relatório de Validação CNDM'
nomePlanilha = 'CNDM'
validarMunicipiosPR(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha)

### FIM DAS VERIFICAÇÕES DO PARANÁ ###

print('Verificação de CNDM finalizada. \nIniciando verificação de relatórios de atividades. \nAguarde...')
nomeRelatorio = 'Relatório de Validação de Atividades'
nomePlanilha = 'Atividades'
validarAtividades(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha, base)

print('Verificação de relatórios de atividades finalizada. \nGerando relatório de documentos não verificados. \nAguarde...')
nomeRelatorio = 'Relatório de documento não avaliados'
nomePlanilha = 'Não-lidos'
verificarInvalidos(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha)

print('Relatório finalizado. \nFim da execução.')

#input('Pessione enter para encerrar...')