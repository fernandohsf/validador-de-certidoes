import os
import sys
import shutil
from AnaliseNfse import validarNFSE
from googleDrive import autenticarGoogleAPI, baixarTodosArquivos, listarArquivosDrive
from Utils import BuscarPastaMesAnterior, atualizarBase, identificacao

#planilhaID = '1L_GtpCUd3_2uNGj8l64s7zr41ajyBUxxtxtVhQ5inLk' # Produção
#diretorioBaseDrive = '1ZinjciG-RUIi_cZxZzi2k-4YaNgm1Gft' # Produção
planilhaID = '1GSSDC9MOqEp3AuQJGe1DD9vV9Crdk7vHQGX9jhlPjOk' # Homologação
diretorioBaseDrive = '1yq5i3L1tHrztWPTiSVrwYKSFgpEy9DDl' # Homologação

service_drive, cliente_gspread = autenticarGoogleAPI()
dadosBaseCadastro, dadosBaseAnalise = atualizarBase(planilhaID, cliente_gspread)

idPastaMesAnterior = BuscarPastaMesAnterior(service_drive, diretorioBaseDrive)
pastas = listarArquivosDrive(service_drive, idPastaMesAnterior)

for pasta in pastas:
    idProfessor, nomeProfessor = identificacao(pasta['name'])
    idPastaProfessor = pasta['id']
    if str(idProfessor) in dadosBaseAnalise:
        status = dadosBaseAnalise[str(idProfessor)].get("Documentos estão aptos para seguir para pagamento?", "Status não encontrado")
        if status == 'Apto' or status == 'Inapto':
            continue

        downloadsTemp = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'Downloads')
        if os.path.exists(downloadsTemp):
            shutil.rmtree(downloadsTemp)
        os.makedirs(downloadsTemp, exist_ok=True)
        arquivos = listarArquivosDrive(service_drive, idPastaProfessor)
        baixarTodosArquivos(service_drive, arquivos, downloadsTemp)

        print('Iniciando verificação de NFSE (Nota fiscal de serviço eletrônica). \nAguarde...')
        validarNFSE(service_drive, cliente_gspread, dadosBaseCadastro, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID)

        print(f'Verificação de relatórios de atividades finalizada.\nVerificação dos documentos do professor {nomeProfessor} finalizada.')

input('Pessione enter para encerrar...')