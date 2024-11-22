from datetime import datetime

def lancamento_controle(id_professor, letra_controle, valido, observacao, valor_nota, numero_nota, cliente_gspread, planilha_ID):
    data = datetime.today().strftime('%d/%m/%Y')

    try:
        planilha = cliente_gspread.open_by_key(planilha_ID).worksheet('Disponível para Análise')
    except Exception as e:
        print(f"Erro ao acessar a planilha: {e}")
        return {}

    # Mapeia os IDs para os índices das linhas na planilha
    mapaId = {cell: index for index, cell in enumerate(planilha.col_values(1), start=1)}

    # Obtém o índice da linha correspondente ao ID
    index = mapaId.get(str(id_professor))

    if index is None:
        return
    
    updates = []

    try:
        if not observacao == 'Existem arquivos de NFSE duplicados. ':
            if letra_controle == 'L':                
                updates.append({
                    'range': f'P{index}',  # Status da coluna P
                    'values': [['Em análise']]
                })
                updates.append({
                    'range': f'{letra_controle}{index}',  # Valor da nota na coluna L
                    'values': [[valor_nota]]
                })
                updates.append({
                    'range': f'Z{index}',  # Número da nota na coluna Z
                    'values': [[numero_nota]]
                })
                if observacao != 'Existem arquivos de NFSE duplicados. ':
                    updates.append({
                        'range': f'P{index}', # Status da coluna P
                        'values': [['Inapto']]
                    })
            else:
                updates.append({
                    'range': f'{letra_controle}{index}',  # Atualizar a célula correspondente à letra de controle
                    'values': [[valido]]
                })

        if letra_controle == 'M':
            if planilha.cell(index, 26).value != '' and planilha.cell(index, 26).value != str(numero_nota): # Z
                observacao += 'O Número da NFS-e no relatório de atividades está diferente da nota. '

            # Verifica se tem todos os 7 documentos
            valores_colunas_h_a_n = planilha.get(f'H{index}:N{index}')[0]  # Obtém a linha como uma lista
            todosDocs = 'Não'
            if all(valor != '' for valor in valores_colunas_h_a_n):
                updates.append({
                    'range': f'O{index}',
                    'values': [['Sim']]
                })
                todosDocs = 'Sim'
            
            if (valores_colunas_h_a_n[0] == 'Sim' and  # H
                valores_colunas_h_a_n[1] == 'Sim' and  # I
                valores_colunas_h_a_n[2] == 'Sim' and  # J
                valores_colunas_h_a_n[3] == 'Sim' and  # K
                valores_colunas_h_a_n[5] == 'Sim' and  # M
                valores_colunas_h_a_n[6] == 'Sim' and  # N
                todosDocs == 'Sim'):
                updates.append({
                    'range': f'P{index}',
                    'values': [['Apto']]
                })

            else:
                updates.append({
                    'range': f'P{index}',
                    'values': [['Inapto']]
                })

        if (observacao != ''):
            observacao = f'\n{data}: {observacao}'
            valor_atual = planilha.cell(index, 19).value or '' 
            
            observacao = valor_atual + observacao
            updates.append({
                'range': f'S{index}',
                'values': [[observacao]]
            })

        planilha.batch_update(updates)

    except Exception  as e:
        if "[429]" in str(e).lower():
            print("Erro: Limite de requisições excedido. Por favor, aguarde um momento antes de tentar novamente.")
        else:
            print(f"Ocorreu um erro ao acessar a planilha: {e}")