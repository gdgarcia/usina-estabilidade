from numpy import sin, tan


def npr(nr, cota_base_montante):
    return nr - cota_base_montante


def area_jq(dist_xj, pzi, pzj):
    return dist_xj * min(pzi, pzj)


def area_jqx(dist_xj):
    return dist_xj / 2.


def area_iq(dist_xi, dist_xj, pzi, pzm):
    return (
        (dist_xi - dist_xj) * min(pzi, pzm)
    )


def area_iqx(dist_xj, dist_xi):
    return (dist_xj + dist_xi) / 2.


def area_mq(dist_xm, dist_xi, npr, pzm):
    return (
        (dist_xm - dist_xi) * min(npr, pzm)
    )


def area_mqx(dist_xi, dist_xm):
    return (dist_xi + dist_xm) / 2.


def area_jt(dist_xj, pzi, pzj):
    return (
        dist_xj * abs(pzi - pzj) / 2.
    )


def area_jtx(pzi, pzj, dist_xj):
    if pzi >= pzj:
        return 2. * dist_xj / 3.
    else:
        return dist_xj / 3.


def area_it(dist_xi, dist_xj, pzm, pzi):
    return (
        (dist_xi - dist_xj) * abs(pzm - pzi) / 2.
    )


def area_itx(pzm, pzi, dist_xi, dist_xj):
    if pzm >= pzi:
        return (2. * dist_xi + dist_xj) / 3.
    else:
        return (dist_xi + 2. * dist_xj) / 3.


def area_mt(dist_xm, dist_xi, npr, pzm):
    return (
        (dist_xm - dist_xi) * abs(npr - pzm) / 2.
    )


def area_mtx(npr, pzm, dist_xm, dist_xi):
    if (npr >= pzm):
        return (2. * dist_xm + dist_xi) / 3.
    else:
        return (dist_xm + 2. * dist_xi) / 3. 


def area_total(area_jq, area_iq, area_mq, area_jt, area_it, area_mt):
    return (
        area_jq + area_iq + area_mq + area_jt + area_it + area_mt
    )


def area_totalx(area_jq, area_jqx, area_iq, area_iqx, area_mq, area_mqx,
                area_jt, area_jtx, area_it, area_itx, area_mt, area_mtx,
                area_total):
    return (
        (area_jq*area_jqx + area_iq*area_iqx + area_mq*area_mqx
         + area_jt*area_jtx + area_it*area_itx + area_mt*area_mtx )/area_total
    )


def v_bloco(volume_bloco):
    return volume_bloco


def xcg_bloco(xcg_bloco):
    return xcg_bloco


def v_enchimento(v_enchimento):
    return v_enchimento


def xcg_enchimento(xcg_enchimento):
    return xcg_enchimento


def v_agua(nr, cota_ogiva, v_agua_poly):
    return v_agua_poly(max(nr, cota_ogiva))


def xcg_agua(nr, cota_ogiva, xcg_agua_poly):
    return xcg_agua_poly(max(nr, cota_ogiva))


def v_sedimento(cota_ogiva, cota_sedimento, largura):
    return (
        0.5 * ((cota_ogiva - cota_sedimento) ** 2) * largura
    )


def xcg_sedimento(cota_ogiva, cota_sedimento, cota_base_jusante):
    return (
        (cota_ogiva - cota_sedimento) / 3. 
        + (cota_sedimento - cota_base_jusante)
    )


def v_empuxo_agua1(nr, pzm, c1=224.95, c2=1.6548, c3=28.125, c4=4.85):
    return (
        (0.5 * (nr - c1)**2 + (c2 * pzm + c3)) * c4
    )


def v_empuxo_agua2(nr, cota_base_montante, c1=18.35):
    return (
        0.5 * c1 * (nr - cota_base_montante)**2
    )


def xcg_empuxo_agua1(nr, pzm, c1=224.95, c2=28.125, c3=0.65903,
                     c4=2.31, c5=2.5, c6=3.75):
    
    f1 = nr - c1
    f2 = c2 - c3 * pzm
    f3 = c4 * pzm

    parc1 = 0.5 * (f1 ** 2)
    parc2 = f1 / 3.
    parc3 = f2 * c5
    parc4 = f3 * c6

    sbt1 = (parc1*parc2 + parc3 + parc4)
    sbt2 = (parc1 + f2 + f3)

    return sbt1 / sbt2


def xcg_empuxo_agua2(nr, cota_base_montante, cota_base_jusante):
    return (
        (nr - cota_base_montante) / 3 
        + (cota_base_montante - cota_base_jusante)
    )


def v_assoreamento(largura, cota_ogiva, cota_terreno):
    return (
        0.5 * largura * ((cota_ogiva - cota_terreno) ** 2)
    )


def xcg_assoreamento(cota_ogiva, cota_terreno, cota_base_jusante):
    return (
        (cota_ogiva - cota_terreno) / 3 + (cota_terreno - cota_base_jusante)
    )


def v_subpressao(area_total, largura):
    return area_total * largura


def xcg_subpressao(area_totalx):
    return area_totalx


def fst(v_bloco, xcg_bloco, gamma_concreto, v_enchimento, xcg_enchimento,
        gamma_enchimento, xcg_agua, v_agua, gamma_agua, v_sedimento,
        xcg_sedimento, gamma_sedimento, v_empuxo_agua1, xcg_empuxo_agua1,
        v_empuxo_agua2, xcg_empuxo_agua2, v_assoreamento, angulo_sedimento,
        xcg_assoreamento, v_subpressao, xcg_subpressao):
    
    sbt1 = (
        v_bloco * xcg_bloco * gamma_concreto
        + v_enchimento * xcg_enchimento * gamma_enchimento
        + xcg_agua * v_agua * gamma_agua
        + v_sedimento * xcg_sedimento * gamma_sedimento
    )

    sbt2 = (
        v_empuxo_agua1 * xcg_empuxo_agua1 * gamma_agua
        + v_empuxo_agua2 * xcg_empuxo_agua2 * gamma_agua
        + (
            v_assoreamento * gamma_sedimento
            * (1 - sin(angulo_sedimento)) / (1 + sin(angulo_sedimento))
            * xcg_assoreamento  # neste caso, xcg_assoremaneto multiplica do numerador

        )
        + v_subpressao * xcg_subpressao * gamma_agua
    )

    return sbt1 / sbt2


def fsd(v_bloco, gamma_concreto, v_enchimento, gamma_enchimento, xcg_agua,
        gamma_agua, v_sedimento, gamma_sedimento, v_subpressao, phi, gamma_phi, 
        c, area, gamma_c, v_empuxo_agua1, v_empuxo_agua2, v_assoreamento,
        angulo_sedimento):
    
    sbt1 = (
        (
            v_bloco * gamma_concreto
            + v_enchimento * gamma_enchimento
            + xcg_agua * gamma_agua
            + v_sedimento * gamma_sedimento
            - v_subpressao * gamma_agua
        )
        * (tan(phi) / gamma_phi)
        + (c * area / gamma_c)
    )

    sbt2 = (
        v_empuxo_agua1 * gamma_agua
        + v_empuxo_agua2 * gamma_agua
        + (
            v_assoreamento * gamma_sedimento
            * (1 - sin(angulo_sedimento)) / (1 + sin(angulo_sedimento))
        )
    )

    return sbt1 / sbt2
