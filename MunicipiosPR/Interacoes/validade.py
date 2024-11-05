from datetime import datetime

def verificarDataValidade(data, dataValidade, valido):
    try:
        if(dataValidade < data):
            valido = 'Não'

        diasValidade = dataValidade - data
        if(0 <= int(diasValidade.days) < 10):
            valido = 'Não'

        dataValidade = datetime.strftime(dataValidade,'%d/%m/%Y')
    except:
        valido = 'Não'

    return valido