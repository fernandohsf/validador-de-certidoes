from datetime import datetime

def identificacao(pasta):
    pasta = pasta.split(' - ')
    id = int(pasta[0])
    nomeEmissor = pasta[1]
    return id, nomeEmissor

def verificar_data_validade(data, dataValidade, valido):
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