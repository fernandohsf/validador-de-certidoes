from openpyxl import load_workbook
from datetime import datetime
import os

def lancamentoControle(id, letraControle, valido, observacao, valorNota, numeroNota):
    data = datetime.strftime(datetime.today(), '%d/%m/%Y')
    #caminhoControle = 'G:/.shortcut-targets-by-id/11ZtAUc2nGNGy2GThmaGwa0im9xgYZtx_/Contratação'
    global relatorioControle, planilhaControle, caminhoControle, arquivoControle, index
    caminhoControle = 'G:\\Meu Drive'
    arquivoControle = 'Cópia de Análise Manual de Documentos.xlsx'

    relatorioControle = load_workbook(os.path.join(caminhoControle, arquivoControle))
    planilhaControle = relatorioControle['Disponível para Análise']

    # Mapeia os IDs para os índices das linhas na planilha
    mapaId = {celula.value: celula.row for celula in planilhaControle['A']}

    # Obtém o índice da linha correspondente ao ID
    index = mapaId.get(id)

    if (index is None):
        return

    if (letraControle == 'L'):
        planilhaControle[letraControle + str(index)] = valorNota
        planilhaControle[f'Z{index}'] = numeroNota
    elif(letraControle == 'M'):
        if(planilhaControle[f'Z{index}'].value != ''):
            if(planilhaControle[f'Z{index}'].value != str(numeroNota)):
                observacao += 'O Número da NFS-e no relatório de atividades está diferente da nota. '
        planilhaControle[letraControle + str(index)] = valido
    else:   
        planilhaControle[letraControle + str(index)] = valido

    if (observacao != ''):
        observacao = f'\n{data}: {observacao}'
        if (planilhaControle[f'S{index}'].value is None):
            planilhaControle[f'S{index}'] = ''
            planilhaControle[f'S{index}'].value = observacao
        else:
            planilhaControle[f'S{index}'].value += observacao

    if (planilhaControle[f'H{index}'].value == 'Sim' and planilhaControle[f'I{index}'].value == 'Sim' and planilhaControle[f'J{index}'].value == 'Sim' and 
        planilhaControle[f'K{index}'].value == 'Sim' and planilhaControle[f'L{index}'].value == 'R$ 1.400,00' and planilhaControle[f'M{index}'].value == 'Sim' and 
        planilhaControle[f'N{index}'].value == 'Sim'
        ):
        planilhaControle[f'P{index}'].value = 'Apto'
    else:
        planilhaControle[f'P{index}'].value = 'Inapto'

    if (planilhaControle[f'H{index}'].value != '' and planilhaControle[f'I{index}'].value != '' and planilhaControle[f'J{index}'].value != '' and 
        planilhaControle[f'K{index}'].value != '' and planilhaControle[f'L{index}'].value != '' and planilhaControle[f'M{index}'].value != '' and 
        planilhaControle[f'N{index}'].value != ''
        ):
        planilhaControle[f'O{index}'].value = 'Sim'


    relatorioControle.save(os.path.join(caminhoControle, arquivoControle))