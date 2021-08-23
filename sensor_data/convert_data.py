from datetime import datetime, time
from django.db.models import Q
from django.db.models import Max as Max_Aggr, Min as Min_Aggr, Avg as Avg_Aggr

from app.models import Usina, Bloco, BlocoData
from .models import BundleData


def convert_bundle_to_block(usina, initial_date=None, end_date=None,
                            delete=True):
    """
    Esta função transforma os dados de bundle em blocos de dados de usinas.
    """
    bundle_qs = _get_bundle_qs(usina, initial_date, end_date)

    bloco_qs = _get_bloco_qs(usina)

    for bundle in bundle_qs:
        # vamos iterar sobre bundle_qs. 
        # quando cada iteracao estiver prontas, podemos deletar o bundle,
        # se assim for escolhido
        for bloco in bloco_qs:
            data = bundle.bundle_data
            nr = _get_nr_value(bundle, bloco)
            pzm = _get_pzm_value(bundle, bloco)
            pzi = _get_pzi_value(bundle, bloco)
            pzj = _get_pzj_value(bundle, bloco)

            BlocoData.objects.update_or_create(
                data=data,
                bloco=bloco,
                nr=nr,
                pzm=pzm,
                pzi=pzi,
                pzj=pzj
            )
        
        if delete:
            bundle.delete()
        else:
            bundle.update(already_converted_to_block_data=True)        


def _get_bundle_qs(usina, initial_date, end_date):

    bundle_qs = BundleData.objects.filter(usina=usina)

    if initial_date is not None:
        init_dt = datetime.combine(initial_date, time(0))
        bundle_qs = bundle_qs.filter(bundle_data__gte=init_dt)
    
    if end_date is not None:
        end_dt = datetime.combine(end_date, time(0))
        bundle_qs = bundle_qs.filter(bundle_data__lte=end_dt)
    
    return bundle_qs


def _get_bloco_qs(usina):

    return Bloco.objects.filter(usina=usina)


def _get_nr_value(bundle, bloco):
    # Neste caso especifico nao usamos bloco. Deveria haver somente 1 valor de
    # nr entre os sensores de 1 pacote de dados.
    return bundle.sensor_data.filter(type='nr').first().value


def _get_pzm_value(bundle, bloco):
    
    pzm0_num = bloco.pz_m_0
    pzm1_num = bloco.pz_m_1
    relation = bloco.pz_m_rel

    if pzm1_num is None:
        return bundle.sensor_data.get(Q(type='pz') & Q(number=pzm0_num)).value
    else:
        pzm_num = (pzm0_num, pzm1_num)

        aggregate_function = _get_aggregate_function(relation)

        return bundle.sensor_data.filter(
            Q(type='pz') & Q(number__in=pzm_num)
        ).aggregate(value=aggregate_function('value'))['value']


def _get_pzi_value(bundle, bloco):
    
    pzi0_num = bloco.pz_i_0
    pzi1_num = bloco.pz_i_1
    relation = bloco.pz_m_rel

    if pzi1_num is None:
        return bundle.sensor_data.get(Q(type='pz') & Q(number=pzi0_num)).value
    else:
        pzi_num = (pzi0_num, pzi1_num)

        aggregate_function = _get_aggregate_function(relation)

        return bundle.sensor_data.filter(
            Q(type='pz') & Q(number__in=pzi_num)
        ).aggregate(value=aggregate_function('value'))['value']


def _get_pzj_value(bundle, bloco):
    pzj0_num = bloco.pz_j_0
    pzj1_num = bloco.pz_j_1
    relation = bloco.pz_m_rel

    if pzj1_num is None:
        return bundle.sensor_data.get(Q(type='pz') & Q(number=pzj0_num)).value
    else:
        pzj_num = (pzj0_num, pzj1_num)

        aggregate_function = _get_aggregate_function(relation)

        return bundle.sensor_data.filter(
            Q(type='pz') & Q(number__in=pzj_num)
        ).aggregate(value=aggregate_function('value'))['value']


def _get_aggregate_function(relation):

    if relation == 'max':
        return Max_Aggr
    elif relation == 'min':
        return Min_Aggr
    else:
        return Avg_Aggr
