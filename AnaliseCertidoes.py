import os
import sys
import time
import shutil
from AnaliseNfse import validarNFSE
from AnaliseCRF_Pj import validarCRF
from AnaliseCNDT_Pj import validarCNDT
from AnaliseCNDU_Pj import validarCNDU
from AnaliseCNDE_PR_Pj import validarCNDE_PR
from AnaliseCNDM_PR import validarMunicipiosPR
from AnaliseRelatorioAtividades import validarAtividades
from Utils import BuscarPastaMesAnterior, atualizarBase, identificacao
from googleDrive import autenticarGoogleAPI, baixarTodosArquivos, listarArquivosDrive

def main():
    #planilhaID = '1L_GtpCUd3_2uNGj8l64s7zr41ajyBUxxtxtVhQ5inLk' # Produção
    #diretorioBaseDrive = '1ZinjciG-RUIi_cZxZzi2k-4YaNgm1Gft' # Produção
    planilhaID = '1GSSDC9MOqEp3AuQJGe1DD9vV9Crdk7vHQGX9jhlPjOk' # Homologação
    diretorioBaseDrive = '1yq5i3L1tHrztWPTiSVrwYKSFgpEy9DDl' # Homologação

    print('Olá.')
    time.sleep(1)
    print('Eu sou o Nexus, o ajudante virtual da FAPEC.')
    time.sleep(1)
    print('Estou aqui para te ajudar a verificar as certidões negativas de débitos que estão em formato PDF.')
    time.sleep(1)
    print('\nVamos começar?')
    time.sleep(2)

    print('\nMe conectando ao google.')
    service_drive, cliente_gspread = autenticarGoogleAPI()
    time.sleep(1)
    print('Buscando informações essenciais para iniciar.')
    dadosBaseCadastro, dadosBaseAnalise = atualizarBase(planilhaID, cliente_gspread)
    idPastaMesAnterior = BuscarPastaMesAnterior(service_drive, diretorioBaseDrive)
    pastas = listarArquivosDrive(service_drive, idPastaMesAnterior)
    time.sleep(1)
    print('Todas as informações foram obtdas com sucesso!')
    time.sleep(1)
    print('\nVou iniciar as análises.')

    for pasta in pastas:
        idProfessor, nomeProfessor = identificacao(pasta['name'])
        idPastaProfessor = pasta['id']
        time.sleep(1)
        print(f'\nVerificando os documentos do professor(a) {idProfessor} - {nomeProfessor}.')
        if str(idProfessor) in dadosBaseAnalise:
            status = dadosBaseAnalise[str(idProfessor)].get("Documentos estão aptos para seguir para pagamento?", "Status não encontrado")
            if status == 'Apto':
                print('Este professor(a) está com o status de APTO na planilha, por isso não irei analisar.\nVou para o próximo da lista.')
                continue
            if status == 'Inapto':
                print('Este professor(a) está com o status de INAPTO na planilha, por isso não irei analisar.\nVou para o próximo da lista.')
                continue

            time.sleep(1)
            print('Fazendo o download dos documentos.')
            downloadsTemp = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'Downloads')
            if os.path.exists(downloadsTemp):
                shutil.rmtree(downloadsTemp)
            os.makedirs(downloadsTemp, exist_ok=True)
            arquivos = listarArquivosDrive(service_drive, idPastaProfessor)
            baixarTodosArquivos(service_drive, arquivos, downloadsTemp)
            time.sleep(1)

            validarNFSE(service_drive, cliente_gspread, dadosBaseCadastro, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID)
            time.sleep(1)
            validarCNDU(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID)
            time.sleep(1)
            validarCNDT(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID)
            time.sleep(1)
            validarCRF(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID)
            time.sleep(1)
            validarCNDE_PR(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID)
            time.sleep(1)
            validarMunicipiosPR(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID)
            time.sleep(1)
            validarAtividades(service_drive, cliente_gspread, dadosBaseCadastro, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID)

            time.sleep(1)
            print(f'Terminei os documentos deste professor(a)\n')

    time.sleep(1)
    print('\nVerificação concluída! Todos os professores disponíveis foram analisados com sucesso.')
    time.sleep(1)
    print('Caso precise de ajuda no futuro, estarei aqui.')
    time.sleep(1)
    input('Pressione a tecla Enter para finalizar o programa e encerrar o Nexus...')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o processo: {e}")
        input("Pressione a tecla Enter para finalizar o programa e encerrar o Nexus...")