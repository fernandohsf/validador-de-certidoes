import os
import sys
import gspread
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload

def autenticarGoogleAPI():
    caminhoExe = os.path.dirname(os.path.abspath(sys.argv[0]))
    caminhoCredenciais = os.path.join(caminhoExe, 'credenciais_google.json')
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    try:
        creds = Credentials.from_service_account_file(caminhoCredenciais, scopes=scope)
        service_drive = build('drive', 'v3', credentials=creds)
        cliente_gspread = gspread.authorize(creds)
        return service_drive, cliente_gspread
    except Exception as e:
        print(f"Erro ao autenticar Google Drive: {e}")
        return None

def listarArquivosDrive(service, idPasta):
    query = f"'{idPasta}' in parents and trashed = false"
    resultados = service.files().list(q=query, fields="files(id, name, modifiedTime)").execute()
    return resultados.get('files', [])

def baixarArquivo(service, idArquivo, nomeArquivo):
    caminhoTemporario = f'G:\\Drives compartilhados\\PROJETOS\\Contratos\\01.CONVENIAR\\21 - Automação de análise jurídica\\Analisador de documentos\\tmp'
    pdfTemporario = os.path(caminhoTemporario, nomeArquivo)
    try:
        request = service.files().get_media(fileId=idArquivo)
        with open(caminhoTemporario, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        fh.close()
    except Exception as e:
        print(f"Erro ao baixar arquivo: {e}")
    return pdfTemporario

def renomearArquivoDrive(service, idArquivo, novoNome, idPasta):
    # Verificar se o arquivo é o que está sendo renomeado
    arquivo_atual = service.files().get(fileId=idArquivo, fields='name').execute()
    nomeAtual = arquivo_atual['name']
    
    if nomeAtual == novoNome:
        return nomeAtual, False
    
    contador = 1
    nomeFinal = novoNome
    
    while arquivoExiste(service, nomeFinal, idPasta):
        # Se o nome já existir, adicionar o sufixo 'Duplicado 01', 'Duplicado 02', etc.
        nomeFinal = f"Duplicado {str(contador).zfill(2)} - {novoNome}"
        contador += 1
    
    # Atualizar o nome do arquivo no Google Drive
    arquivo_atualizado = {'name': nomeFinal}
    service.files().update(
        fileId=idArquivo,
        body=arquivo_atualizado,
        fields='id, name'
    ).execute()

    return contador > 1

def arquivoExiste(service, nomeArquivo, idPasta):
    # Verifica se já existe um arquivo com o mesmo nome na pasta especificada
    query = f"name = '{nomeArquivo}' and '{idPasta}' in parents and trashed = false"
    resultados = service.files().list(q=query, fields="files(id, name)").execute()
    arquivos = resultados.get('files', [])
    return len(arquivos) > 0