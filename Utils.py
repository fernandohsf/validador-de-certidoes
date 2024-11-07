import time
from datetime import date

def atualizarBase(planilhaID, cliente_gspread, nexusApi):
    nexusApi.enviar_mensagem('Informações do google planilhas...')
    try:
        planilha_cadastro = cliente_gspread.open_by_key(planilhaID).worksheet('Cadastro')
        linhas_cadastro = planilha_cadastro.get_all_values()
        
        # Acessa a planilha Análise
        planilha_analise = cliente_gspread.open_by_key(planilhaID).worksheet('Disponível para Análise')
        linhas_analise = planilha_analise.get_all_values()

    except Exception as e:
        nexusApi.enviar_mensagem(f"Erro ao acessar as planilhas: {e}")
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

    # Processa dados da planilha Disponível para Análise
    cabecalho_analise = linhas_analise[0]
    colunasExtraidasAnalise = ['ID', 'Documentos estão aptos para seguir para pagamento?']
    indicesColunasAnalise = [cabecalho_analise.index(coluna) for coluna in colunasExtraidasAnalise]

    dadosBaseAnalise = {
        linha[indicesColunasAnalise[0]]: {
            colunasExtraidasAnalise[i]: linha[indicesColunasAnalise[i]] for i in range(1, len(colunasExtraidasAnalise))
        }
        for linha in linhas_analise[1:]
    }
    nexusApi.enviar_mensagem('Feito.')
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

def BuscarPastaMesAnterior(service, idDiretorioBase, nexusApi):
    nexusApi.enviar_mensagem('Informações do google drive...')
    anoVigente = date.today().year
    mesAnterior = date.today().month-1
    anoAbreviado = date.today().strftime('%y')
    mes = ['Dez', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov']

    # Buscar a pasta do ano corrente ou anterior (caso o mês seja janeiro)
    pastaAnual = anoVigente if mesAnterior != 0 else anoVigente - 1
    
    idPastaAnual = buscarPasta(service, str(pastaAnual), idPastaPai=idDiretorioBase)
    if not idPastaAnual:
        nexusApi.enviar_mensagem(f"Pasta do ano {pastaAnual} não encontrada.")
        return None
    
    idPastaAnalise = buscarPasta(service, 'Análise de Documentos' ,idPastaPai=idPastaAnual)
    if not idPastaAnalise:
        nexusApi.enviar_mensagem("Pasta 'Análise de Documentos' não encontrada.")
        return None
    
    idPastaEmail = buscarPasta(service, 'e-Mail', idPastaPai=idPastaAnalise)
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
    
    idPastaMesAnterior = buscarPasta(service, nome_pasta, idPastaPai=idPastaEmail)

    nexusApi.enviar_mensagem('Feito.')    
    return idPastaMesAnterior

def identificacao(pasta):
    pasta = pasta.split(' - ')
    id = int(pasta[0])
    nomeEmissor = pasta[1]
    return id, nomeEmissor