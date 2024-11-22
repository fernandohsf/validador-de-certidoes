import time

def atualizarBase(planilhaID, cliente_gspread, nexusApi):
    nexusApi.enviar_mensagem('Informações do google planilhas...')
    try:
        planilha_cadastro = cliente_gspread.open_by_key(planilhaID).worksheet('Cadastro')
        linhas_cadastro = planilha_cadastro.get_all_values()
        
        # Acessa a planilha Análise
        planilha_analise = cliente_gspread.open_by_key(planilhaID).worksheet('Disponível para Análise')
        linhas_analise = planilha_analise.get_all_values()

    except Exception as e:
        nexusApi.enviar_mensagem(f"Não consegui acessar, Erro ao acessar as planilhas: {e}")
        return {}, {}

    # Processa dados da planilha Cadastro
    cabecalho_cadastro = linhas_cadastro[0]
    colunasExtraidasCadastro = ['ID', 'Nome', 'CNPJ', 'Valor a receber']
    if all(coluna in cabecalho_cadastro for coluna in colunasExtraidasCadastro):
        indicesColunasCadastro = [cabecalho_cadastro.index(coluna) for coluna in colunasExtraidasCadastro]

        dadosBaseCadastro = {
            linha[indicesColunasCadastro[0]]: {
                colunasExtraidasCadastro[i]: linha[indicesColunasCadastro[i]] for i in range(1, len(colunasExtraidasCadastro))
            }
            for linha in linhas_cadastro[1:]
        }
    else:
        nexusApi.enviar_mensagem('Não consegui extrair os dados. ')
        time.sleep(1)
        nexusApi.enviar_mensagem('Por favor, verifique se o cabeçalho das colunas da planilha Gestão Professor Formador, na aba "Cadastro" estão com nomes corretos.')
        time.sleep(1)

    # Processa dados da planilha Disponível para Análise
    cabecalho_analise = linhas_analise[0]
    colunasExtraidasAnalise = ['ID', 'Documentos estão aptos para seguir para pagamento?']
    if all(coluna in cabecalho_analise for coluna in colunasExtraidasAnalise):
        indicesColunasAnalise = [cabecalho_analise.index(coluna) for coluna in colunasExtraidasAnalise]
        
        dadosBaseAnalise = {
            linha[indicesColunasAnalise[0]]: {
                colunasExtraidasAnalise[i]: linha[indicesColunasAnalise[i]] for i in range(1, len(colunasExtraidasAnalise))
            }
            for linha in linhas_analise[1:]
        }
        nexusApi.enviar_mensagem('Feito.')
    else:
        nexusApi.enviar_mensagem('Não consegui extrair os dados. ')
        time.sleep(1)
        nexusApi.enviar_mensagem('Por favor, verifique se se o cabeçalho das colunas da planilha Gestão Professor Formador, na aba "Disponível para Análise" estão com nomes corretos.')
        time.sleep(1)

    return dadosBaseCadastro, dadosBaseAnalise