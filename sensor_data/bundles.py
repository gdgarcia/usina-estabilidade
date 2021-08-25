# Módulo para criar as funções que irão salvar os dados como Bundles e
# transformar os bundles em dados das usinas
from django.db.utils import IntegrityError

from app.models import Usina, Bloco, BlocoData
from sensor_data.models import BundleData, SensorData


def save_bundle(dados, campos, usina, update=False):
    """
    Funcao para salvar os dados como bundles e dados de sensores na base de
    dados

    dados: dicionario de dicionarios: a chave principal é um data
    (usada no bundle). Os dicionarios internos tem os campos a serem utilizados
    para os sensores desse campo
    campos: lista com os campos presentes nos dicionarios internos
    usina: apps.models.Usina. usina a ser utilizada como foreign key para todos
    os dados a serem salvos
    update: se os dados devem ser atualizados em caso de dados ja presentes na
    DB (restricao de singularidade violada)
    """

    # quantidade de elementos criados
    created_counter = 0
    # quantidade de elementos atualizados
    updated_counter = 0

    tipos_e_numeros = _tipos_e_numeros_de_campos(campos)

    to_be_created, to_be_updated, data_dict = _prepare_data(dados, usina)

    # atualizar somente se pedido (update) e
    # se necessario (len(to_be_updated) != 0)
    if update and len(to_be_updated) != 0:
        bundles_updated = BundleData.objects.filter(
            usina=usina, bundle_data__in=to_be_updated
        )
        sensors_to_be_updated = []
        for bundle in bundles_updated:
            bundle.already_converted_to_block_data = False
            sensors = bundle.sensor_data.all()
            for sensor in sensors:
                if sensor.type == 'nr':
                    sensor_str = sensor.type
                else:
                    sensor_str = ''.join((sensor.type, str(sensor.number)))
                new_value = data_dict[bundle.bundle_data]['dados'][sensor_str]
                sensor.value = new_value
                sensors_to_be_updated.append(sensor)
        BundleData.objects.bulk_update(bundles_updated,
                                       ['already_converted_to_block_data'])
        SensorData.objects.bulk_update(sensors_to_be_updated, ['value'])

    # criar somente se for necessario (len(to_be_created) != 0)
    if len(to_be_created) != 0:
        # criando de uma vez todos os BundleData
        BundleData.objects.bulk_create(
            [BundleData(usina=usina, bundle_data=data)
             for data in to_be_created]
        )
        bundles_created = BundleData.objects.filter(
            usina=usina, bundle_data__in=to_be_created
        )
        sensors_to_be_created = []
        for bundle in bundles_created:
            # para cada bundle criado, criando de uma vez os dados de sensores
            sensors_to_be_created.extend(
                [SensorData(
                    bundle_data=bundle,
                    data=bundle.bundle_data,
                    type=tipos_e_numeros[campo][0],
                    number=tipos_e_numeros[campo][1],
                    value=valor,
                ) for campo, valor
                    in data_dict[bundle.bundle_data]['dados'].items()]
            )
        # vamos criar todos os dados de sensores de uma so vez
        SensorData.objects.bulk_create(sensors_to_be_created)

    created_counter = len(to_be_created)
    updated_counter = len(to_be_updated)

    # retornando o numero de elementos criados e atualizados
    return created_counter, updated_counter


def _tipos_e_numeros_de_campos(campos):

    tipos_e_numeros = dict()

    for campo in campos:
        if len(campo) == 2:
            tipos_e_numeros[campo] = ('nr', 1)
        else:
            tipos_e_numeros[campo] = (campo[:2], int(campo[2:]))
    return tipos_e_numeros


def _prepare_data(dados, usina):
    """
    Separa os dados entre aqueles que devem ser atualizados e aqueles que
    devem ser criados.
    Retorna duas listas (dados a serem criados e dados a serem atualizados)
    e retorna um dicionario com os ids dos dados a serem atualizados
    """
    data = list(dados.keys())

    updatable = BundleData.objects.filter(usina=usina, bundle_data__in=data)

    update_bundle = [bundle.bundle_data for bundle in updatable]

    bundle_insert_data = {
        bundle.bundle_data: 
        {'id': bundle.id, 'dados': dados[bundle.bundle_data]}
         for bundle in updatable
    }

    create_bundle = []
    for dt in data:
        if dt not in bundle_insert_data:
            bundle_insert_data[dt] = {'id': None, 'dados': dados[dt]}
            create_bundle.append(dt)
    

    return create_bundle, update_bundle, bundle_insert_data
