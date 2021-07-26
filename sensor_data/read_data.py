import csv
import re

from dateutil import parser
from io import TextIOWrapper
from zipfile import ZipFile


def _get_only_files_with_extension(list_of_files, extension):

    files_names_and_paths = []

    re_extension = re.compile(f'.{extension}$')

    for file in list_of_files:
        if re_extension.search(file):
            name = file.split('/')[-1]
            files_names_and_paths.append((file, name))
    
    return files_names_and_paths


def _float_parser(data, convert_commas_to_point=False): 
    if convert_commas_to_point:
        return float(data.replace(',', '.'))
    
    return float(data)


def _parse_datetime(dt_str, ignoretz=True, dayfirst=False):

    return parser.parse(dt_str, ignoretz=ignoretz, dayfirst=dayfirst)


def _piezometro_medicao(key1, key2, entry):
    if key2 is None:
        # piezometro automatizado
        return _float_parser(entry[key1]) / 9.8
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


def _treat_reservatorio_data(data, convert_commas_to_points=False):
    """
    Trata os dados do reservatorio e os retorna ordenados por data
    """
    treated = []

    data_key = list(filter(lambda x: 'data' in x.lower(), data[0].keys()))[0]
    nr_key = list(filter(lambda x: 'montante' in x.lower(), data[0].keys()))[0]
    for entry in data:
        treated.append(
            {'data': _parse_datetime(entry[data_key]),
             'nr': _float_parser(entry[nr_key], convert_commas_to_points)}
        )

    return sorted(treated, key=lambda x: x['data'])


def _treat_piezo_data(data, autom_data=False):
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
            {'data': _parse_datetime(entry[data_key], dayfirst=dayfirst),
             'pz': _piezometro_medicao(piez1_key, piez2_key, entry)}
        )
    return sorted(treated, key=lambda x: x['data'])


def _treat_data_from_folder(folder_data):
    
    for data in folder_data['data']:
        
        if data['data_type'] == 'reservatorio':
            data['treated'] = _treat_reservatorio_data(data['data'])
        elif data['data_type'] == 'piezometro':
            data['treated'] = _treat_piezo_data(data['data'],
                                               autom_data=data['autom'])
        
    return folder_data


def read_data_from_folder(zipped_folder, encoding='utf-8', extension='csv',
                          auto_data_marker='autom',
                          auto_data_separator=',',
                          auto_decimal_separator='.',
                          man_data_separator=';',
                          man_decimal_separator=','):
    """
    Procura todos os arquivos .csv da pasta e le os arquivos de nivel de
    reservatorio e piezometro
    """

    re_piezo = re.compile('^PZ(?P<piezo>\d+)([a-zA-Z_.]*).csv$', re.ASCII)
    re_reservatorio = re.compile('reservatorio', re.IGNORECASE)

    folder_data = {'data': []}
    
    with ZipFile(zipped_folder) as zip_list:
        files_and_names = _get_only_files_with_extension(zip_list.namelist(),
                                                         extension)
        for file_path, file_name in files_and_names:
            data = {'file_name': file_name}
            if (res := re_piezo.search(file_name)):
                # arquivo classificado como um piezometro
                data['data_type'] = 'piezometro'
                data['number'] = int(res.group('piezo'))
                data['autom'] = True if auto_data_marker in file_name else False
                data['delimiter'] = (
                    auto_data_separator if data['autom'] else man_data_separator
                )
                data['decimal'] = (
                    auto_decimal_separator if data['autom']
                    else man_decimal_separator
                )
            elif (res := re_reservatorio.search(file_name)):
                data['data_type'] = 'reservatorio'
                data['data_number'] = None
                data['autom'] = True
                data['delimiter'] = auto_data_separator
                data['decimal'] = auto_decimal_separator
            else:
                data['data_type'] = None
                data['number'] = None
                data['autom'] = None
                data['delimiter'] = auto_data_separator
                data['decimal'] = man_data_separator
            
            with zip_list.open(file_path, 'r') as fp:
                data['data'] = [
                    row for row in csv.DictReader(
                        TextIOWrapper(fp,encoding=encoding),
                        delimiter=data['delimiter']
                    )
                ]

            folder_data['data'].append(data)

    return _treat_data_from_folder(folder_data)
