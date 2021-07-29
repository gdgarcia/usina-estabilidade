# Módulo para criar as funções que irão salvar os dados como Bundles e
# transformar os bundles em dados das usinas


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


def save_bundle(dados, campos, usina):
    """
    Funcao para salvar os dados como bundles e dados de sensores na base de
    dados

    dados: dicionario de dicionarios: a chave principal é um data
    (usada no bundle). Os dicionarios internos tem os campos a serem utilizados
    para os sensores desse campo
    campos: lista com os campos presentes nos dicionarios internos
    usina: apps.models.Usina. usina a ser utilizada como foreign key para todos
    os dados a serem salvos
    """

    bundle_ids = []

    tipos_e_numeros = _tipos_e_numeros_de_campos(campos)

    for data, dado in dados.items():
        bundle = BundleData.objects.create(
            usina=usina, bundle_data=data,
            already_converted_to_block_data=False
        )
        for campo, valor in dado.items():
            tipo, numero = tipos_e_numeros[campo]
            SensorData.objects.create(
                bundle_data=bundle, data=data,
                type=tipo, number=numero, value=valor
        )
        
        bundle_ids.append(bundle.id)
    # retornando os ids dos bundles criados para, eventualmente, serem
    # transformados em Bloco de Dados
    return bundle_ids
