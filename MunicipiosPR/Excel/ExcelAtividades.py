import xlsxwriter

def criarExcel(nomeRelatorio, nomePlanilha):
    global relatorio
    relatorio = xlsxwriter.Workbook(nomeRelatorio)
    global planilha 
    planilha = relatorio.add_worksheet(nomePlanilha)
     
    cabecalho = (
        'Data da verficação', 
        'Nome do arquivo verificado',
        'Data de modificação',
        'ID',
        'Nome (emissor)',
        'CNPJ',
        'Período de realização',
        'Data assinatura',
        'Número nota',
        'Válida',
        'Observação'
    )
    incluirNoExcel(0, 0, cabecalho)

def incluirNoExcel(linhaExcel, colunaExcel, conteudo):
    for item in (conteudo):
        formatacao = relatorio.add_format()
        formatacao.set_bold(False)
        formatacao.set_bg_color('white')
        formatacao.set_font_color('black')
        formatacao.set_font_size(11)
        formatacao.set_border()
        formatacao.set_border_color('#D3D3D3')   
        if(item == 'Apto'):
            formatacao.set_bold(False)
            formatacao.set_bg_color('#228B22')
            formatacao.set_font_color('white')
            formatacao.set_font_size(11)
        if(item == 'Inapto'):
            formatacao.set_bold(False)
            formatacao.set_bg_color('#FF0000')
            formatacao.set_font_color('white')
            formatacao.set_font_size(11)
        if(linhaExcel == 0):
            formatacao.set_bold()
            formatacao.set_bg_color('#4F4F4F')
            formatacao.set_font_color('white')
            formatacao.set_font_size(12)  
        planilha.write(linhaExcel, colunaExcel, item, formatacao)
        colunaExcel+= 1   

def fecharExcel():
    planilha.autofit()
    relatorio.close()