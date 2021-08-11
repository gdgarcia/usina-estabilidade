# Módulo para criar as funções que irão salvar os dados como Bundles e
# transformar os bundles em dados das usinas
from django.db.utils import IntegrityError

from app.models import Usina, Bloco, BlocoData
from sensor_data.models import BundleData, SensorData


def _tipos_e_numeros_de_campos(campos):

    tipos_e_numeros = dict()

    for campo in campos:
        if len(campo) == 2:
            tipos_e_numeros[campo] = ('nr', 1)
        else:
            tipos_e_numeros[campo] = (campo[:2], int(campo[2:]))
    
    return tipos_e_numeros


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

    if update:
        for data, dado in dados.items():
            bundle, created = BundleData.objects.update_or_create(
                usina=usina, bundle_data=data,
                already_converted_to_block_data=False
            )
            for campo, valor in dado.items():
                tipo, numero = tipos_e_numeros[campo]
                SensorData.objects.update_or_create(
                    bundle_data=bundle, data=data,
                    type=tipo, number=numero, value=valor
                )

            if created:
                created_counter += 1
            else:
                updated_counter += 1

    else:  # somente criar dados novos. ignorar os ja existentes
        # somente queremos criar itens que nao existem.
        # nao queremos atualizar se existirem.
        for data, dado in dados.items():
            bundle, created = BundleData.objects.get_or_create(
                usina=usina, bundle_data=data
            )
            # somente tratamos os criados.
            # se ja existir, nao fazemos nada
            if created:
                bundle.already_converted_to_block_data = False
                bundle.save()
                for campo, valor in dado.items():
                    tipo, numero = tipos_e_numeros[campo]
                    SensorData.objects.create(
                        bundle_data=bundle, data=data,
                        type=tipo, number=numero, value=valor
                    )
                created_counter += 1

    # retornando o numero de elementos criados e atualizados
    return created_counter, updated_counter
