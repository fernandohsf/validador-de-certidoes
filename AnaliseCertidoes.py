import time
from datetime import date
from AnaliseNfse import validarNFSE
from AnaliseCNDU_Pj import validarCNDU
from AnaliseCNDT_Pj import validarCNDT
from AnaliseCRF_Pj import validarCRF
from AnaliseCNDE_PR_Pj import validarCNDE_PR
from AnaliseCNDM_PR import validarMunicipiosPR
from AnaliseRelatorioAtividades import validarAtividades
from CertidoesInvalidas import verificarInvalidos

diretorioAvaliacao = 'G:/Drives compartilhados/PROJETOS/Contratos/01.CONVENIAR/21 - Automação de análise jurídica/Notas e certidões'
#diretorioAvaliacao = 'D:\\Downloads'
diretorioRelatorio = 'G:\\Drives compartilhados\\PROJETOS\\Contratos\\01.CONVENIAR\\21 - Automação de análise jurídica\\Relatórios de análise'

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
validarNFSE(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha)

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
validarAtividades(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha)

print('Verificação de relatórios de atividades finalizada. \nGerando relatório de documentos não verificados. \nAguarde...')
nomeRelatorio = 'Relatório de documento não avaliados'
nomePlanilha = 'Não-lidos'
verificarInvalidos(diretorioAvaliacao, diretorioRelatorio, nomeRelatorio, nomePlanilha)

print('Relatório finalizado. \nFim da execução.')
time.sleep(2)
 