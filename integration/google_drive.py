import os
import sys
import time
import gspread
from datetime import date
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload

def autenticar_google_API(nexusApi):
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
        time.sleep(1)
        nexusApi.enviar_mensagem('Conectei com sucesso!')
        return service_drive, cliente_gspread
    except Exception as e:
        nexusApi.enviar_mensagem(f"Erro ao autenticar Google Drive: {e}")
        return None

def listar_arquivos_drive(service, idPasta):
    query = f"'{idPasta}' in parents and trashed = false"
    resultados = service.files().list(q=query, fields="files(id, name, modifiedTime)").execute()
    return resultados.get('files', [])

def baixar_todos_arquivos(service, arquivos, pastaTemp, nexusApi):
    for arquivo in arquivos:
        if not arquivo['name'].lower().endswith('.pdf'):
            continue

        arquivoTemp = os.path.join(pastaTemp, f"{arquivo['id']}.pdf")
        try:
            request = service.files().get_media(fileId=arquivo['id'])
            with open(arquivoTemp, "wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
            fh.close()
        except Exception as e:
            nexusApi.enviar_mensagem(f"Não consegui fazer o download do arquivo: {arquivo['name']}.")
    nexusApi.enviar_mensagem('Download concluído.')

def renomear_arquivo_drive(service, idArquivo, novoNome, idPasta):
    # Verificar se o arquivo é o que está sendo renomeado
    arquivo_atual = service.files().get(fileId=idArquivo, fields='name').execute()
    nomeAtual = arquivo_atual['name']
    
    if nomeAtual == novoNome:
        return nomeAtual, False
    
    contador = 1
    nomeFinal = novoNome
    
    while arquivo_existe(service, nomeFinal, idPasta):
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

    return nomeFinal, contador > 1

def arquivo_existe(service, nomeArquivo, idPasta):
    # Verifica se já existe um arquivo com o mesmo nome na pasta especificada
    query = f"name = '{nomeArquivo}' and '{idPasta}' in parents and trashed = false"
    resultados = service.files().list(q=query, fields="files(id, name)").execute()
    arquivos = resultados.get('files', [])
    return len(arquivos) > 0

def buscar_pasta(service, nomePasta, idPastaPai=None):
    query = f"name = '{nomePasta}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if idPastaPai:
        query += f" and '{idPastaPai}' in parents"

    resultados = service.files().list(q=query, fields="files(id, name)").execute()
    arquivos = resultados.get('files', [])
    
    if arquivos:
        return arquivos[0]['id']  # Retorna o ID da primeira pasta encontrada
    return None

def buscar_pasta_mes_anterior(service, idDiretorioBase, nexusApi):
    nexusApi.enviar_mensagem('Informações do google drive...')
    anoVigente = date.today().year
    mesAnterior = date.today().month-1
    anoAbreviado = date.today().strftime('%y')
    mes = ['Dez', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov']

    # Buscar a pasta do ano corrente ou anterior (caso o mês seja janeiro)
    pastaAnual = anoVigente if mesAnterior != 0 else anoVigente - 1
    
    idPastaAnual = buscar_pasta(service, str(pastaAnual), idPastaPai=idDiretorioBase)
    if not idPastaAnual:
        nexusApi.enviar_mensagem(f"Pasta do ano {pastaAnual} não encontrada.")
        return None
    
    idPastaAnalise = buscar_pasta(service, 'Análise de Documentos' ,idPastaPai=idPastaAnual)
    if not idPastaAnalise:
        nexusApi.enviar_mensagem("Pasta 'Análise de Documentos' não encontrada.")
        return None
    
    idPastaEmail = buscar_pasta(service, 'e-Mail', idPastaPai=idPastaAnalise)
    if not idPastaEmail:
        nexusApi.enviar_mensagem("Pasta 'e-Mail' não encontrada.")
        return None    
    
    for mesPasta in mes:
        if mesAnterior == 0:
            nome_pasta = f'{mesPasta}/{int(anoAbreviado) - 1}'
            break
        if mesAnterior == mes.index(mesPasta):
            nome_pasta = f'{mesPasta}/{anoAbreviado}'
            break
    
    idPastaMesAnterior = buscar_pasta(service, nome_pasta, idPastaPai=idPastaEmail)

    nexusApi.enviar_mensagem('Feito.')    
    return idPastaMesAnterior