import os
import sys
import time
import shutil
from AnaliseNfse import validarNFSE
from googleDrive import autenticarGoogleAPI, baixarTodosArquivos, listarArquivosDrive
from Utils import BuscarPastaMesAnterior, atualizarBase, identificacao

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
    print('Vou pegar as informações necessárias agora.')
    dadosBaseCadastro, dadosBaseAnalise = atualizarBase(planilhaID, cliente_gspread)
    idPastaMesAnterior = BuscarPastaMesAnterior(service_drive, diretorioBaseDrive)
    pastas = listarArquivosDrive(service_drive, idPastaMesAnterior)
    time.sleep(1)
    print('Todas as informações foram obtdas com sucesso!')
    time.sleep(1)
    print('Vou iniciar as análises.')

    for pasta in pastas:
        idProfessor, nomeProfessor = identificacao(pasta['name'])
        idPastaProfessor = pasta['id']
        time.sleep(1)
        print(f'\nVerificando os documentos do professor(a) {idProfessor} - {nomeProfessor}.')
        if str(idProfessor) in dadosBaseAnalise:
            status = dadosBaseAnalise[str(idProfessor)].get("Documentos estão aptos para seguir para pagamento?", "Status não encontrado")
            if status == 'Apto':
                print('Este professor(a) está com o status de APTO na planilha, por isso não irei analisar.\nVou para o próximo da lista.\n')
                continue
            if status == 'Inapto':
                print('Este professor(a) está com o status de INAPTO na planilha, por isso não irei analisar.\nVou para o próximo da lista.\n')
                continue

            time.sleep(1)
            print('Fazendo o download dos documentos.')
            downloadsTemp = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'Downloads')
            if os.path.exists(downloadsTemp):
                shutil.rmtree(downloadsTemp)
            os.makedirs(downloadsTemp, exist_ok=True)
            arquivos = listarArquivosDrive(service_drive, idPastaProfessor)
            baixarTodosArquivos(service_drive, arquivos, downloadsTemp)

            print('\nIniciando análise da NFSE (Nota fiscal de serviço eletrônica). \nAguarde...')
            validarNFSE(service_drive, cliente_gspread, dadosBaseCadastro, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID)
            print('Análise concluída.')

            time.sleep(1)
            print(f'Terminei os documentos do professor(a) {idProfessor}-{nomeProfessor}.\n')

            
    print('Finalizei a verificação de todos os professores que estavam disponíveis para análise.')
    time.sleep(1)
    print('Até a próxima.')
    input('Pessione a tecla enter para encerrar...')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        input("Pressione Enter para fechar...")