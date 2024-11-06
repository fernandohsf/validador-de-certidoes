import os
import sys
import threading
import time
import shutil
import webview 
from AnaliseNfse import validarNFSE
from AnaliseCRF_Pj import validarCRF
from AnaliseCNDT_Pj import validarCNDT
from AnaliseCNDU_Pj import validarCNDU
from AnaliseCNDE_PR_Pj import validarCNDE_PR
from AnaliseCNDM_PR import validarMunicipiosPR
from AnaliseRelatorioAtividades import validarAtividades
from Utils import BuscarPastaMesAnterior, atualizarBase, identificacao
from googleDrive import autenticarGoogleAPI, baixarTodosArquivos, listarArquivosDrive

class NexusAPI:
    def __init__(self):
        self.window = None

    def enviar_mensagem(self, mensagem):
        if self.window:
            mensagem_formatada = mensagem.replace("\n", "<br>")
            self.window.evaluate_js(f"adicionarMensagem('{mensagem_formatada}')")

    def interface_carregada(self):
        self.interface_pronta = True
        self.enviar_mensagem('Interface carregada com sucesso!')
        self.iniciar_analise()

    def iniciar_analise(self):
        
        #planilhaID = '1L_GtpCUd3_2uNGj8l64s7zr41ajyBUxxtxtVhQ5inLk' # Produção
        #diretorioBaseDrive = '1ZinjciG-RUIi_cZxZzi2k-4YaNgm1Gft' # Produção
        planilhaID = '1GSSDC9MOqEp3AuQJGe1DD9vV9Crdk7vHQGX9jhlPjOk' # Homologação
        diretorioBaseDrive = '1yq5i3L1tHrztWPTiSVrwYKSFgpEy9DDl' # Homologação

        self.enviar_mensagem('Olá.')
        time.sleep(1)
        self.enviar_mensagem('Eu sou o Nexus, o ajudante virtual da FAPEC.')
        time.sleep(1)
        self.enviar_mensagem('Estou aqui para te ajudar a verificar as certidões negativas de débitos que estão em formato PDF.')
        time.sleep(1)
        self.enviar_mensagem('Vamos começar?')
        time.sleep(2)

        self.enviar_mensagem('Me conectando ao google.')
        service_drive, cliente_gspread = autenticarGoogleAPI(self)
        time.sleep(1)
        self.enviar_mensagem('Buscando informações essenciais para iniciar.')
        dadosBaseCadastro, dadosBaseAnalise = atualizarBase(planilhaID, cliente_gspread, self)
        idPastaMesAnterior = BuscarPastaMesAnterior(service_drive, diretorioBaseDrive, self)
        pastas = listarArquivosDrive(service_drive, idPastaMesAnterior)
        time.sleep(1)
        self.enviar_mensagem('Todas as informações foram obtdas com sucesso!')
        time.sleep(1)
        self.enviar_mensagem('Vou iniciar as análises.')

        for pasta in pastas:
            idProfessor, nomeProfessor = identificacao(pasta['name'])
            idPastaProfessor = pasta['id']
            time.sleep(1)
            self.enviar_mensagem(f'Verificando os documentos do(a) professor(a) {idProfessor} - {nomeProfessor}.')
            if str(idProfessor) in dadosBaseAnalise:
                status = dadosBaseAnalise[str(idProfessor)].get("Documentos estão aptos para seguir para pagamento?", "Status não encontrado")
                if status == 'Apto':
                    self.enviar_mensagem('O(a) professor(a) está com o status de APTO na planilha, por isso não irei analisar.\nVou para o próximo da lista.')
                    continue
                if status == 'Inapto':
                    self.enviar_mensagem('O(a) professor(a) está com o status de INAPTO na planilha, por isso não irei analisar.\nVou para o próximo da lista.')
                    continue

                time.sleep(1)
                self.enviar_mensagem('Fazendo o download dos documentos.')
                downloadsTemp = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'Downloads')
                if os.path.exists(downloadsTemp):
                    shutil.rmtree(downloadsTemp)
                os.makedirs(downloadsTemp, exist_ok=True)
                arquivos = listarArquivosDrive(service_drive, idPastaProfessor)
                baixarTodosArquivos(service_drive, arquivos, downloadsTemp, self)
                time.sleep(1)

                validarNFSE(service_drive, cliente_gspread, dadosBaseCadastro, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID, self)
                time.sleep(1)
                validarCNDU(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID, self)
                time.sleep(1)
                validarCNDT(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID, self)
                time.sleep(1)
                validarCRF(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID, self)
                time.sleep(1)
                validarCNDE_PR(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID, self)
                time.sleep(1)
                validarMunicipiosPR(service_drive, cliente_gspread, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID, self)
                time.sleep(1)
                validarAtividades(service_drive, cliente_gspread, dadosBaseCadastro, downloadsTemp, idPastaProfessor, idProfessor, nomeProfessor, planilhaID, self)

                time.sleep(1)
                self.enviar_mensagem(f'Terminei os documentos deste professor(a)\n')

        time.sleep(1)
        self.enviar_mensagem('Verificação concluída! Todos os professores disponíveis foram analisados com sucesso.')
        time.sleep(1)
        self.enviar_mensagem('Caso precise de ajuda no futuro, estarei aqui.')
        time.sleep(1)
        #input('Pressione a tecla Enter para finalizar o programa e encerrar o Nexus...')

def iniciar_interface():
    api = NexusAPI()
    window = webview.create_window('Nexus - Assistente Virtual', 'src\\index.html')
    api.window = window
    threading.Thread(target=api.iniciar_analise).start()
    webview.start()

if __name__ == "__main__":
    iniciar_interface()