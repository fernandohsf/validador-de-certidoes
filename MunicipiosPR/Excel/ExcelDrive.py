import os
import sys
import gspread
from datetime import datetime
from gspread.exceptions import APIError
from google.oauth2.service_account import Credentials

def lancamentoControle(id, letraControle, valido, observacao, valorNota, numeroNota):
    data = datetime.strftime(datetime.today(), '%d/%m/%Y')

    caminhoBase = os.path.dirname(os.path.abspath(sys.argv[0]))
    caminho_credenciais = os.path.join(caminhoBase, 'credenciais_google.json')
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(caminho_credenciais, scopes=scope)
    cliente = gspread.authorize(creds)

    planilhaID = '1L_GtpCUd3_2uNGj8l64s7zr41ajyBUxxtxtVhQ5inLk' # Produção
    #planilhaID = '1GSSDC9MOqEp3AuQJGe1DD9vV9Crdk7vHQGX9jhlPjOk' # Homologação
    planilha = cliente.open_by_key(planilhaID).worksheet('Disponível para Análise')

    # Mapeia os IDs para os índices das linhas na planilha
    mapaId = {cell: index for index, cell in enumerate(planilha.col_values(1), start=1)}

    # Obtém o índice da linha correspondente ao ID
    index = mapaId.get(str(id))

    if index is None:
        return
    
    try:
        if letraControle == 'L':
            planilha.update(f'P{index}', [['Em análise']])
            planilha.update(f'{letraControle}{index}', [[valorNota]])
            planilha.update(f'Z{index}', [[numeroNota]])
            if observacao != '':
                planilha.update(f'P{index}', [['Inapto']])

        elif letraControle == 'M':
            if planilha.cell(index, 26).value != '': # Z
                if planilha.cell(index, 26).value != str(numeroNota):
                    observacao += 'O Número da NFS-e no relatório de atividades está diferente da nota. '
            planilha.update(f'{letraControle}{index}', [[valido]])
        else:   
            planilha.update(f'{letraControle}{index}', [[valido]])

        if (observacao != ''):
            observacao = f'\n{data}: {observacao}'
            valor_atual = planilha.cell(index, 19).value # S
        
            if valor_atual is None:
                valor_atual = ''
            
            observacao = valor_atual + observacao
            planilha.update(f'S{index}', [[observacao]])

        valores_colunas_h_a_n = planilha.get(f'H{index}:N{index}')[0]  # Obtém a linha como uma lista

        if letraControle == 'M':
            # Verifica se tem todos os 7 documentos
            todosDocs = 'Não'
            if all(valor != '' for valor in valores_colunas_h_a_n):
                planilha.update(f'O{index}', [['Sim']])
                todosDocs = 'Sim'
            
            if (valores_colunas_h_a_n[0] == 'Sim' and  # H
                valores_colunas_h_a_n[1] == 'Sim' and  # I
                valores_colunas_h_a_n[2] == 'Sim' and  # J
                valores_colunas_h_a_n[3] == 'Sim' and  # K
                valores_colunas_h_a_n[5] == 'Sim' and  # M
                valores_colunas_h_a_n[6] == 'Sim' and  # N
                todosDocs == 'Sim'):
                planilha.update(f'P{index}', [['Apto']])

            else:
                planilha.update(f'P{index}', [['Inapto']])
    except APIError as e:
        if "[429]" in str(e).lower():
            print("Erro: Limite de requisições excedido. Por favor, aguarde um momento antes de tentar novamente.")
        else:
            print(f"Ocorreu um erro ao acessar a planilha: {e}")