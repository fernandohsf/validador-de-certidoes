import os
import sys
import time
import shutil
import webview 
import win32gui
from Utils import identificacao
from integration.google_drive import buscar_pasta_mes_anterior, autenticar_google_API, baixar_todos_arquivos, listar_arquivos_drive
from repository.sheets_repository import atualizar_base
from services.Analise_CNDE_PR_Pj import validar_CNDE_PR
from services.Analise_CNDM_PR import validar_Municipios_PR
from services.Analise_CNDT_Pj import validar_CNDT
from services.Analise_CNDU_Pj import validar_CNDU
from services.Analise_CRF_Pj import validar_CRF
from services.Analise_Nfse import validar_NFSE
from services.Analise_relatorio_atividades import validar_atividades

class NexusAPI:
    def __init__(self):
        self.window = None
        self.hwnd = None  # Inicializa o hwnd
        self.is_dragging = False  # Inicializa o atributo is_dragging
    
    def set_window_handle(self):
        # Define o handle da janela do PyWebview usando o título
        self.hwnd = win32gui.FindWindow(None, "Nexus - Assistente Virtual")

    def start_drag(self, x, y):
        if not self.hwnd:
            self.set_window_handle()

        # Obtém a posição atual da janela
        rect = win32gui.GetWindowRect(self.hwnd)
        self.offset_x = x - rect[0]
        self.offset_y = y - rect[1]
        self.is_dragging = True

    def drag(self, x, y):
        if self.is_dragging and self.hwnd:
            largura = win32gui.GetWindowRect(self.hwnd)[2] - win32gui.GetWindowRect(self.hwnd)[0]
            altura = win32gui.GetWindowRect(self.hwnd)[3] - win32gui.GetWindowRect(self.hwnd)[1]
            win32gui.MoveWindow(self.hwnd, x - self.offset_x, y - self.offset_y, largura, altura, True)

    def stop_drag(self):
        self.is_dragging = False

    def enviar_mensagem(self, mensagem):
        if self.window:
            mensagem_formatada = mensagem.replace("\n", "<br>")
            self.window.evaluate_js(f"adicionarMensagem('{mensagem_formatada}')")
    
    def adicionar_botao(self, id_botao, texto_botao, funcao):
        if self.window:
            html_botao = f'<button id="{id_botao}" class="botao-interacao" onclick="{funcao}">{texto_botao}</button>'
            self.window.evaluate_js(f"document.getElementById('mensagens').innerHTML += '{html_botao}';")
            self.window.evaluate_js('document.getElementById("mensagens").scrollTop = document.getElementById("mensagens").scrollHeight;')

    def saudacao(self):
        self.enviar_mensagem('Olá.')
        time.sleep(1)
        self.enviar_mensagem('Eu sou o Nexus, o ajudante virtual da FAPEC.')
        time.sleep(1)
        self.enviar_mensagem('Estou aqui para te ajudar a verificar as certidões negativas de débitos que estão em formato PDF.')
        time.sleep(1)
        self.enviar_mensagem('Vamos começar?')
        time.sleep(1)
        self.adicionar_botao('btn-iniciar-analise', 'Iniciar análise', 'window.pywebview.api.iniciar_analise()')

    def encerramento(self):
        self.enviar_mensagem('Caso precise de ajuda no futuro, estarei aqui.')
        time.sleep(1)
        self.enviar_mensagem('Até a próxima.')
        time.sleep(3)
        if self.window:
            self.window.destroy()
        
    def minimizar_tela(self):
        if self.window:
            self.window.minimize()

    def iniciar_analise(self):
        self.window.evaluate_js('document.getElementById("btn-iniciar-analise").disabled = true;')
        #planilha_ID = '1L_GtpCUd3_2uNGj8l64s7zr41ajyBUxxtxtVhQ5inLk' # Produção
        #diretorio_base_drive = '1ZinjciG-RUIi_cZxZzi2k-4YaNgm1Gft' # Produção
        planilha_ID = '1GSSDC9MOqEp3AuQJGe1DD9vV9Crdk7vHQGX9jhlPjOk' # Homologação
        diretorio_base_drive = '1yq5i3L1tHrztWPTiSVrwYKSFgpEy9DDl' # Homologação

        self.enviar_mensagem('Buscando informações essenciais para iniciar.')
        time.sleep(1)
        try:
            dados_base_cadastro, dados_base_analise = atualizar_base(planilha_ID, self.cliente_gspread, self)
            id_pasta_mes_anterior = buscar_pasta_mes_anterior(self.service_drive, diretorio_base_drive, self)
            pastas = listar_arquivos_drive(self.service_drive, id_pasta_mes_anterior)
            time.sleep(1)
            self.enviar_mensagem('Todas as informações foram obtdas com sucesso!')
            time.sleep(1)
            self.enviar_mensagem('Vou iniciar as análises.')

            for pasta in pastas:
                id_professor, nome_professor = identificacao(pasta['name'])
                id_pasta_professor = pasta['id']
                time.sleep(1)
                self.enviar_mensagem(f'Consultando cadastro de:\n<b>ID:</b> {id_professor}. <b>Nome:</b> {nome_professor}.')
                downloads_temp = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'Downloads')
                if os.path.exists(downloads_temp):
                    shutil.rmtree(downloads_temp)

                if str(id_professor) in dados_base_analise:
                    status = dados_base_analise[str(id_professor)].get("Documentos estão aptos para seguir para pagamento?")
                    if status == 'Apto':
                        self.enviar_mensagem('Seu status está definido como APTO na planilha, por isso não irei analisar.\nVou para o próximo da lista.')
                        continue
                    if status == 'Inapto':
                        self.enviar_mensagem('Seu status está definido como INAPTO na planilha, por isso não irei analisar.\nVou para o próximo da lista.')
                        continue

                    time.sleep(1)
                    self.enviar_mensagem('Fazendo o download dos documentos.')
                    os.makedirs(downloads_temp, exist_ok=True)
                    arquivos = listar_arquivos_drive(self.service_drive, id_pasta_professor)
                    baixar_todos_arquivos(self.service_drive, arquivos, downloads_temp, self)
                    time.sleep(1)

                    self.enviar_mensagem('Analisando os documentos.')
                    validar_NFSE(self.service_drive, self.cliente_gspread, dados_base_cadastro, downloads_temp, id_pasta_professor, id_professor, nome_professor, planilha_ID)
                    time.sleep(1)
                    validar_CNDU(self.service_drive, self.cliente_gspread, downloads_temp, id_pasta_professor, id_professor, nome_professor, planilha_ID)
                    time.sleep(1)
                    validar_CNDT(self.service_drive, self.cliente_gspread, downloads_temp, id_pasta_professor, id_professor, nome_professor, planilha_ID)
                    time.sleep(1)
                    validar_CRF(self.service_drive, self.cliente_gspread, downloads_temp, id_pasta_professor, id_professor, nome_professor, planilha_ID)
                    time.sleep(1)
                    validar_CNDE_PR(self.service_drive, self.cliente_gspread, downloads_temp, id_pasta_professor, id_professor, nome_professor, planilha_ID)
                    time.sleep(1)
                    validar_Municipios_PR(self.service_drive, self.cliente_gspread, downloads_temp, id_pasta_professor, id_professor, nome_professor, planilha_ID)
                    time.sleep(1)
                    validar_atividades(self.service_drive, self.cliente_gspread, dados_base_cadastro, downloads_temp, id_pasta_professor, id_professor, nome_professor, planilha_ID)

                    time.sleep(1)
                    self.enviar_mensagem(f'Terminei os documentos deste professor(a)')

            time.sleep(1)
            self.enviar_mensagem('Verificação concluída! Todos os professores disponíveis foram analisados com sucesso.')
            time.sleep(1)
            self.enviar_mensagem('Se houver novos documentos podemos reiniciar a análise ou podemos somente encerrar.')
            time.sleep(1)
            self.enviar_mensagem('O que quer fazer?')
            time.sleep(1)
            self.adicionar_botao('btn-reiniciar-analise', 'Reiniciar análise', 'window.pywebview.api.iniciar_analise()')
            self.adicionar_botao('btn-encerrar', 'Encerrar', 'showTelaConfirmacao()')
        except:
            self.enviar_mensagem('Gostaria de tentar novamente?')
            self.adicionar_botao('btn-reiniciar-analise', 'Reiniciar análise', 'window.pywebview.api.iniciar_analise()')

def iniciar_interface():
    largura = 800
    altura = 600
    api = NexusAPI()

    service_drive, cliente_gspread = autenticar_google_API(api)
    api.service_drive = service_drive
    api.cliente_gspread = cliente_gspread

    window = webview.create_window('Nexus - Assistente Virtual', 'web\\index.html', width=largura, height=altura, frameless=True, resizable=False)
    api.window = window
    window.expose(api.start_drag, api.drag, api.stop_drag, api.enviar_mensagem, api.iniciar_analise, api.encerramento, api.minimizar_tela)
    window.events.loaded += api.saudacao
    webview.start()

if __name__ == "__main__":
    iniciar_interface()