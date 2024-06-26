from datetime import datetime

def verificarDataValidade(data, dataValidade, apto, valido):
    try:
        if(dataValidade < data):
            apto = 'Inapto'
            valido = 'Não'

        diasValidade = dataValidade - data
        if(0 <= int(diasValidade.days) < 5):
            valido = 'Não'
        diasValidade = int(diasValidade.days)
        dataValidade = datetime.strftime(dataValidade,'%d/%m/%Y')
    except:
        apto = 'Inapto'
        valido = 'Não'
        diasValidade = dataValidade = '-'
    return diasValidade, dataValidade, apto, valido