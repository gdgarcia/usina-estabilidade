# Campos a serem exportados de blocodata para apresentacao em tabela

"""
Retornando todos as propiedades de uma classe
properties = inspect.getmembers(BlocoData, lambda o: isinstance(o, property))
1. usaremos isso para testar
2. isso também retornar pk (que deve ser uma propriedade automaticamente gerado) 
"""

blocodata_properties = [
    ('npr', ''),
    ('area_jq', ''),
    ('area_jqx', ''),
    ('area_iq', ''),
    ('area_iqx', ''),
    ('area_mq', ''),
    ('area_mqx', ''),
    ('area_jt', ''),
    ('area_jtx', ''),
    ('area_it', ''),
    ('area_itx', ''),
    ('area_mt', ''),
    ('area_mtx', ''),
    ('area_total', ''),
    ('area_totalx', ''),
    ('v_bloco', ''),
    ('xcg_bloco', ''),
    ('v_enchimento', ''),
    ('xcg_enchimento', ''),
    ('v_agua', ''),
    ('xcg_agua', ''),
    ('v_sedimento', ''),
    ('xcg_sedimento', ''),
    ('v_empuxo_agua1', ''),
    ('v_empuxo_agua2', ''),
    ('xcg_empuxo_agua1', ''),
    ('xcg_empuxo_agua2', ''),
    ('v_assoreamento', ''),
    ('xcg_assoreamento', ''),
    ('v_subpressao', ''),
    ('xcg_subpressao', ''),
    ('fst', ''),
    ('fsd', ''),
]
