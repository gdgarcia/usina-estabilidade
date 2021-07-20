from copy import deepcopy, copy
from bisect import bisect_left
from datetime import datetime, timedelta
from statistics import mean
from dateutil import tz


TZ_INFO = tz.gettz('America/Sao_Paulo')


def _get_closest_date_or_new(key, dt_ordered, tol):
    """
    Procura por uma data proxima na lista dt_ordered.
    Se ha, retorna essa data
    Se nao ha, insere nova chave e retorna
    """
    best_idx = bisect_left(dt_ordered, key)

    if best_idx == 0:
        closest_idx = best_idx
    elif best_idx == len(dt_ordered):
        closest_idx = best_idx - 1
    else:
        dt1 = dt_ordered[best_idx]
        dt2 = dt_ordered[best_idx - 1]
        closest_idx = (best_idx if abs(key - dt1) <= abs(key - dt2)
                       else best_idx - 1)
    
    dt_closest = dt_ordered[closest_idx]
    if abs(key - dt_closest) <= tol:
        return dt_closest, dt_ordered
    else:
        dt_ordered.insert(best_idx, key)
        return key, dt_ordered


def _get_closest_date_or_none(key, dt_ordered, tol):
    """
    Procura por uma data proxima na lista dt_ordered.
    Se ha, retorna essa data
    Se nao ha, retorna none
    """
    best_idx = bisect_left(dt_ordered, key)

    if best_idx == 0:
        closest_idx = best_idx
    elif best_idx == len(dt_ordered):
        closest_idx = best_idx - 1
    else:
        dt1 = dt_ordered[best_idx]
        dt2 = dt_ordered[best_idx - 1]
        closest_idx = (best_idx if abs(key - dt1) <= abs(key - dt2)
                       else best_idx - 1)
    
    dt_closest = dt_ordered[closest_idx]
    if abs(key - dt_closest) <= tol:
        return dt_closest
    else:
        return None


def _recalculate_keys(out):

    new_out = {}
    
    new_dt_ordered = []

    for val in out.values():

        ts_lst = [entry['data'].timestamp() for entry in val]

        dt_min = datetime.fromtimestamp(min(ts_lst)).replace(tzinfo=TZ_INFO)

        dt_mean = datetime.fromtimestamp(mean(ts_lst)).replace(tzinfo=TZ_INFO)

        dt_max = datetime.fromtimestamp(max(ts_lst)).replace(tzinfo=TZ_INFO)
        
        new_key = dt_mean.date()

        new_dt_ordered.append((new_key, dt_min, dt_mean, dt_max, val))
    
    new_dt_ordered.sort(key=lambda x: x[0])

    for new_key, dt_min, dt_mean, dt_max, val in new_dt_ordered:
        new_out[new_key] = {'dt_min': dt_min, 'dt_mean': dt_mean,
                            'dt_max': dt_max,  'data': val}

    return new_out


def get_min_max_dt(data, tol):
    """
    Temos dois conjuntos de dados:
    1. Dados automozatizados
    2. Dados manuais

    - Pegar limites dos dados automatizados (max_dt_auto, min_dt_auto)
    - Pegar limites dos dados manuais (max_dt_man, min_dt_man)
    - Adotar uma tolerância (em dias): default: 30 dias
    
    a. Calculo do valor maximo geral:
        se max_dt_auto >= max_dt_man: retorna max_dt_auto
        caso contrario: retorna min(max_dt_auto + tol, max_dt_man)
    
    b. Calculo do valor minimo geral:
        se min_dt_auto <= min_dt_man: retorna min_dt_auto
        caso contrario: retorna max(min_dt_auto - tol, min_dt_man)
    """

    min_dt_auto_lst = []
    max_dt_auto_lst = []
    min_dt_man_lst = []
    max_dt_man_lst = []


    for entry in data:
        if entry['autom']:
            min_dt_auto_lst.append(entry['treated'][0]['data'])
            max_dt_auto_lst.append(entry['treated'][-1]['data'])
        else:
            min_dt_man_lst.append(entry['treated'][0]['data'])
            max_dt_man_lst.append(entry['treated'][-1]['data'])
            

    min_dt_auto, min_dt_man = min(min_dt_auto_lst), min(min_dt_man_lst)
    max_dt_auto, max_dt_man = max(max_dt_auto_lst), max(max_dt_man_lst)

    # limite maximo de data:
    if max_dt_auto >= max_dt_man:
        max_dt_inter = max_dt_auto
    else:
        max_dt_inter  = min(max_dt_auto + tol, max_dt_man)
    
    #limite minimo de data:
    if min_dt_auto <= min_dt_man:
        min_dt_inter = min_dt_auto
    else:
        min_dt_inter = max(min_dt_auto - tol, min_dt_man)

    return min_dt_inter, max_dt_inter


def get_dam_data(data):
    """
    Obter os dados de reservatorio.
    Retorna um dicionario com as entradas dos dados de reservatorio
    """
    
    for entry in data:
        if entry['data_type'] == 'reservatorio':
            return deepcopy(entry)


def get_piez_auto_man(data):
    """
    Obter os dados de piezometros automatizados.
    Retorna duas listas: uma com os dados dos piezometros automatizados,
        a outra com os dados dos piezometros manuais.
    """
    
    piez_auto = []
    piez_man = []
    
    for entry in data:
        if entry['data_type'] == 'piezometro':
            if entry['autom']:
                piez_auto.append(entry)
            else:
                piez_man.append(entry)
    
    return deepcopy(piez_auto), deepcopy(piez_man)


def aggregate_pz_man(pz_man, min_dt, max_dt, tol_days=4):
    """
    Agregando primeiro os dados de piezometros manuais 
    Hipotese principal> cada
    """

    tol = timedelta(days=tol_days)

    out = dict()

    dt_ordered = []

    first_pz = True
    for pz in pz_man:
        name = 'pz'
        number = pz['number']
        if first_pz:
            # nao ha nenhuma entrada no dicionario
            # nao precisamos checar nada
            first_pz = False
            for pz_entry in pz['treated']:
                dt = pz_entry['data']
                if dt >= min_dt and dt <= max_dt:
                    # somente calculamos dados com datas validas
                    key = dt.date()
                    val = pz_entry['pz']
                    out[key] = [{name: val, 'number': number , 'data': dt}]
            # inserindo na lista ordernada os valores adequados
            dt_ordered.extend(sorted(out.keys()))
        else:
            # ja ha entrada nos dicionarios. somente temos de avaliar se a key
            # ja existe
            for pz_entry in pz['treated']:
                dt = pz_entry['data']
                if dt >= min_dt and dt <= max_dt:
                    key = dt.date()
                    val = pz_entry['pz']
                    key, dt_ordered = _get_closest_date_or_new(key, dt_ordered,
                                                               tol)
                    if key in out:
                        out[key].append({name: val, 'number': number ,
                                         'data': dt})
                    else:
                        # se a data nao esta na lista, devemos saber se ha
                        # alguma proxima (tol) para inserirmos ou entao entrar
                        # com dados novos
                        out[key] = [{name: val, 'number': number ,
                                     'data': dt}]

    out = _recalculate_keys(out)

    return out


def aggregate_dam(dam, min_dt, max_dt):
    """
    Transforma os dados de usinas: cria um dicionario cujas chaves sao as datas
    de entrada dos dados de niveis de reservatorios.

    Retorna somente os dados que então dentro dos limites minimos e maximos de
    data.
    """
    # os dados ja estao ordenados. Nao precisamos mais ordena-los
    treated = dam['treated']

    # retornando os dados somente dentro dos limites de datas
    out = {data['data']: {'nr': data['nr']} for data in treated
            if (data['data'] >= min_dt and data['data'] <= max_dt)}

    return out


def aggregate_pz_auto(out_dam, pz_auto, min_dt, max_dt, tol_hours=1):
    """
    Agregando os dados de piezometros automatizados com os dados de
    reservatorio. Por ambos serem automatizados, as frequencias dos dados sao
    equivalentes.
    """

    failed = dict()
    dt_list = list(out_dam.keys())
    tol = timedelta(seconds=tol_hours*3600)
    out = deepcopy(out_dam)

    for pz in pz_auto:
        failed_pz = dict()
        name = ''.join(('pz', str(pz['number'])))
        pz_data = pz['treated']
        for entry in pz_data:
            data, pz_val = entry['data'], entry['pz']
            if (data >= min_dt and data <= max_dt):
                #somente trataremos os dados que estiverem dentro dos limites
                # minimos e maximos de datas
                if data in out:
                    # data presente. Vamos inserir normalmente
                    out[data].update({name: pz_val})
                else:
                    # Verificar se os dados mais proximos estao dentro da
                    # tolerancia
                    closest_dt = _get_closest_date_or_none(data, dt_list, tol)
                    if closest_dt is not None:
                        out[closest_dt].update({name: pz_val})
                    else:
                        failed_pz[data] = {'closest_data': closest_dt,
                                           'pz': pz_val}
        failed[pz['number']] = failed_pz

    return out, failed


def insert_man_into_auto(out_dam_pz_auto, out_pz_man, tol_days=30):
    """Insere os dados manuais coletados aos dados automaticos.
    A tecnica utilizada e persistencia (os ultimos dados manuais
    preenchem os dados ate a proxima medicao estar presente.
    O limite e 30 dias).
    """
    out_dam_pz_auto_man = deepcopy(out_dam_pz_auto)
    
    tol = timedelta(days=tol_days)
    
    auto_dt_lst = [key for key in out_dam_pz_auto.keys()]
    man_dt_lst = [(key, val['dt_max']) for key, val in out_pz_man.items()]
    
    insert_idx = []
    
    auto_len = len(auto_dt_lst)
    max_len_already_inserted = False
    last_idx = 0
    
    for key_man, man_dt in man_dt_lst:
        idx = bisect_left(auto_dt_lst, man_dt, lo=last_idx)
        last_idx = idx
        if idx != 0:
            # se o indice e zero, nao fazemos nada.
            if idx < auto_len:
                # se o indice for menor que o tamanho, ainda podemos encontrar
                # indices maiores. somente inserimos os dados no vetor
                insert_idx.append((idx, man_dt, key_man))
            else:
                # o indice encontrado é igual ao tamanho do vetor. pegamos o
                # primeiro valor nessa situacao os demais so estarao, 
                # possivelmente, ainda mais no futuro
                if not max_len_already_inserted:
                    max_len_already_inserted = True
                    insert_idx.append((idx, man_dt, key_man))
                    # breaking. only the first is needed
                    break
    
    last_idx = 0
    
    for idx, man_dt, key_man in insert_idx:
        man_data = out_pz_man[key_man]['data']
        for auto_idx in range(last_idx, idx):
            key_auto = auto_dt_lst[auto_idx]
            for pz_man in man_data:
                name = ''.join(('pz', str(pz_man['number'])))
                out_dam_pz_auto_man[key_auto][name] = pz_man['pz']
        last_idx = idx        
    
    return out_dam_pz_auto_man


def filter_incomplete_data(out, instruments_count):
    failed = {}
    for key, val in out.items():
        if len(val) < instruments_count:
            failed[key] = deepcopy(out[key])

    return out, failed


def aggregate_data(data, dt_tol_hours=2):
    """
    Agrega os dados em entradas classificadas por datas e os retorna para o
    usuário.
    O modo de agregar usado é persistência para os dados manuais
    (dados automatizados serão carregados com os últimos dados viáveis de
    medições manuais)
    - Hipotese muito importante: sempre as medicoes de campanha acontecem.
    """

    tol_min_max_days = timedelta(days=30)
    tol_hours = timedelta(seconds=dt_tol_hours*3600)

    # numero total de medicoes que devem estar em cada dado.
    # se houver menos, medicao incompleta. 

    instruments_count = len(data)

    min_dt, max_dt = get_min_max_dt(data, tol_min_max_days)

    dam = get_dam_data(data)
    pz_auto, pz_man = get_piez_auto_man(data)

    out_pz_man = aggregate_pz_man(pz_man, min_dt, max_dt)
    out_dam = aggregate_dam(dam, min_dt, max_dt)
    out_dam_pz_auto, failed_auto = aggregate_pz_auto(out_dam, pz_auto,
                                                     min_dt, max_dt,
                                                     tol_hours=1)


    out = insert_man_into_auto(out_dam_pz_auto, out_pz_man)

    out_filtered, failed = filter_incomplete_data(out, instruments_count)

    return out_filtered, failed, failed_auto
