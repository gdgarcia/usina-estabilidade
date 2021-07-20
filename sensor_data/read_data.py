import os
import glob
import csv
import re

from dateutil import parser, tz


def read_data_from_folder(folder_path, encoding='utf-8'):
    """
    Procura todos os arquivos .csv da pasta e le os arquivos de nivel de reservatorio e piezometro
    """

    csv_path = os.path.join(folder_path, '*.csv')
    csv_files = glob.glob(csv_path)

    re_piezo = re.compile('^PZ(?P<piezo>\d+)([a-zA-Z_.]*).csv$', re.ASCII)
    re_reservatorio = re.compile('reservatorio', re.IGNORECASE)
    
    folder_data = {'folder': folder_path, 'data': []}
    
    for csv_file in csv_files:
        _, file_name = os.path.split(csv_file)
        data = {'file_name': file_name}
        if (res := re_piezo.search(file_name)):
            # arquivo classificado como um piezometro
            data['data_type'] = 'piezometro'
            data['number'] = int(res.group('piezo'))
            data['autom'] = True if 'autom' in file_name else False
            delimiter = ',' if data['autom'] else ';'
        elif (res := re_reservatorio.search(file_name)):
            data['data_type'] = 'reservatorio'
            data['data_number'] = None
            data['autom'] = True
            delimiter = ','
        else:
            data['data_type'] = None
            data['number'] = None
            data['autom'] = None
            delimiter = ','
        
        with open(csv_file, 'r', encoding=encoding) as fp:
            data['data'] = [row for row in csv.DictReader(fp, delimiter=delimiter)]

        folder_data['data'].append(data)
        
    return folder_data


def float_parser(data, convert_commas_to_point=False): 
    if convert_commas_to_point:
        return float(data.replace(',', '.'))
    
    return float(data)


def parse_datetime(dt_str, ignoretz=True, dayfirst=False):
    
    timezone = tz.gettz('America/Sao_Paulo')
    
    return parser.parse(dt_str, ignoretz=ignoretz, dayfirst=dayfirst).replace(tzinfo=timezone)


def piezometro_medicao(key1, key2, entry):
    if key2 is None:
        # piezometro automatizado
        return float_parser(entry[key1]) / 9.8
    else:
        # piezometro nao automatizado
        val1, val2 = (float(entry[key1].replace(',', '.')),
                      float(entry[key2].replace(',', '.')))
        if val1 != 0.0:
            # pegar o primeiro valor, se nao for zero
            return val1
        else:
            # retornar 
            return val2 / 10.


def treat_reservatorio_data(data, convert_commas_to_points=False):
    """
    Trata os dados do reservatorio e os retorna ordenados por data
    """
    treated = []
    
    data_key = list(filter(lambda x: 'data' in x.lower(), data[0].keys()))[0]
    nr_key = list(filter(lambda x: 'montante' in x.lower(), data[0].keys()))[0]
    for entry in data:
        treated.append(
            {'data': parse_datetime(entry[data_key]),
             'nr': float_parser(entry[nr_key], convert_commas_to_points)}
        )
    
    return sorted(treated, key=lambda x: x['data'])


def treat_piezo_data(data, autom_data=False):
    """
    Trata os dados de piezometros e os retorna ordenados por data
    """
    treated = []
    
    data_key = list(filter(lambda x: 'data' in x.lower(), data[0].keys()))[0]
    
    if autom_data:
        piez1_key = list(filter(lambda x: 'leitura' in x.lower(), data[0].keys()))[0]
        piez2_key = None
    else:
        piez1_key = list(filter(lambda x: 'leitura' in x.lower(), data[0].keys()))[0]
        piez2_key = list(filter(lambda x: 'pressão' in x.lower(), data[0].keys()))[0]
    
    for entry in data:
        dayfirst = not autom_data  # False se piezo e automatico. Vardeiro em caso contrario.
        treated.append(
            {'data': parse_datetime(entry[data_key], dayfirst=dayfirst),
             'pz': piezometro_medicao(piez1_key, piez2_key, entry)}
        )
    return sorted(treated, key=lambda x: x['data'])


def treat_data_from_folder(folder_data):
    
    for data in folder_data['data']:
        
        if data['data_type'] == 'reservatorio':
            data['treated'] = treat_reservatorio_data(data['data'])
        elif data['data_type'] == 'piezometro':
            data['treated'] = treat_piezo_data(data['data'],
                                               autom_data=data['autom'])
        
    return folder_data
