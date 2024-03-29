from numpy.polynomial.polynomial import Polynomial
from django.db import models
from django.urls import reverse

from . import stability_equations as stab_eqs


class Usina(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(max_length=100, blank=True, null=True)
    min_fst = models.FloatField(default=1.0)
    min_fsd = models.FloatField(default=1.0)
    qtd_sensores = models.IntegerField(default=1)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('app:usina_detail', kwargs={'pk': self.id})


class Bloco(models.Model):

    TIPO_BLOCO_CHOICES = [
        (None, 'Escolha o tipo do bloco'),
        (1, 'Tipo Blocos 2-4'),
        (2, 'Tipo Blocos 6-15'),
        (3, 'Tipo Bloco 5'),
    ]

    nome = models.CharField(max_length=50)
    usina = models.ForeignKey(
        Usina,
        on_delete=models.CASCADE,
        related_name='blocos',
    )
    tipo = models.IntegerField(
        choices=TIPO_BLOCO_CHOICES,
        default=1,
        verbose_name='Tipo do Bloco'
    )
    volume_bloco = models.FloatField(
        verbose_name='Volume Bloco [m3]'
    )
    xcg_bloco = models.FloatField(
        verbose_name='Xcg Bloco [m]'
    )
    largura = models.FloatField(
        verbose_name='Largura [m]'
    )
    comprimento = models.FloatField(
        verbose_name='Comprimento [m]'
    )
    area = models.FloatField(
        verbose_name='Area [m2]'
    )
    cota_base_montante = models.FloatField(
        verbose_name='Cota da base de montante [m]'
    )
    cota_base_jusante = models.FloatField(
        verbose_name='Cota da base jusante [m]'
    )
    cota_ogiva = models.FloatField(
        verbose_name='Cota da ogiva [m]'
    )
    cota_sedimento = models.FloatField(
        verbose_name='Cota do sedimento [m]'
    )
    cota_terreno = models.FloatField(
        verbose_name='Cota do terreno [m]'
    )
    v_enchimento = models.FloatField(
        verbose_name='Volume do enchimento [m3]'
    )
    xcg_enchimento = models.FloatField(
        verbose_name='Xcg do enchimento [m]'
    )
    dist_xm = models.FloatField(
        verbose_name='Distacia Xm [m]'
    )
    dist_xi = models.FloatField(
        verbose_name='Distacia Xi [m]'
    )
    dist_xj = models.FloatField(
        verbose_name='Distacia Xj [m]'
    )
    gamma_concreto = models.FloatField(
        verbose_name='Gamma do concreto [kN/m3]'
    )
    gamma_agua = models.FloatField(
        verbose_name='Gamma da água [kN/m3]'
    )
    gamma_enchimento = models.FloatField(
        verbose_name='Gamma do enchimento [kN/m3]'
    )
    gamma_sedimento = models.FloatField(
        verbose_name='Gamma do sedimento [kN/m3]'
    )
    phi = models.FloatField(
        verbose_name='Phi [rad]'
    )
    c = models.FloatField(
        verbose_name='c [kN/m2]'
    )
    gamma_phi = models.FloatField(
        verbose_name='Gamma-Phi'
    )
    gamma_c = models.FloatField(
        verbose_name='Gamma-C'
    )
    angulo_sedimento = models.FloatField(
        verbose_name='Ângulo Sedimento [rad]'
    )

    # campos para selecao dos piezometros

    ESCOLHAS_RELACAO = [
        ('min', 'Mínimo entre piezômetros'),
        ('max', 'Máximo entre piezômetros'),
        ('avg', 'Média entre piezômetros'),
    ]

    pz_m_0 = models.IntegerField()
    pz_m_rel = models.CharField(max_length=3, choices=ESCOLHAS_RELACAO,
                                verbose_name='Escolha relação - Piezômetros m')
    pz_m_1 = models.IntegerField(null=True, blank=True)

    pz_i_0 = models.IntegerField()
    pz_i_rel = models.CharField(max_length=3, choices=ESCOLHAS_RELACAO,
                                verbose_name='Escolha relação - Piezômetros i')
    pz_i_1 = models.IntegerField(null=True, blank=True)

    pz_j_0 = models.IntegerField()
    pz_j_rel = models.CharField(max_length=3, choices=ESCOLHAS_RELACAO,
                                verbose_name='Escolha relação - Piezômetros j')
    pz_j_1 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} | {self.usina}"

    def get_absolute_url(self):
        return reverse('app:bloco_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ('usina', 'nome')
        unique_together = ['nome', 'usina']


class NrVolCoeff(models.Model):
    bloco = models.OneToOneField(
        Bloco,
        on_delete=models.CASCADE,
        related_name='nr_vol_coeff',
        primary_key=True
    )
    vol_c0 = models.FloatField(verbose_name='Volume água c0',
                               help_text='coeficiente ordem 0: nr^0')
    vol_c1 = models.FloatField(verbose_name='Volume água c1',
                               help_text='coeficiente ordem 1: nr^1')
    vol_c2 = models.FloatField(verbose_name='Volume água c2',
                               help_text='coeficiente ordem 2: nr^2')

    def __str__(self):
        return f"nr-vol-coeffs | {self.bloco}"
    
    @property
    def poly(self):
        return Polynomial([self.vol_c0, self.vol_c1, self.vol_c2])


class NrXcgCoeff(models.Model):
    bloco = models.OneToOneField(
        Bloco,
        on_delete=models.CASCADE,
        related_name='nr_xcg_coeff',
        primary_key=True
    )
    xcg_c0 = models.FloatField(verbose_name='Xcg água c0',
                               help_text='coeficiente ordem 0: nr^0')
    xcg_c1 = models.FloatField(verbose_name='Xcg água c1',
                               help_text='coeficiente ordem 1: nr^1')
    xcg_c2 = models.FloatField(verbose_name='Xcg água c2',
                               help_text='coeficiente ordem 2: nr^2')
    xcg_c3 = models.FloatField(verbose_name='Xcg água c3',
                               help_text='coeficiente ordem 3: nr^3')

    def __str__(self):
        return f"nr-xcg-coeffs | {self.bloco}"

    @property
    def poly(self):
        return Polynomial([self.xcg_c0, self.xcg_c1, self.xcg_c2, self.xcg_c3])


class BlocoData(models.Model):
    data = models.DateTimeField(db_index=True)
    bloco = models.ForeignKey(
        Bloco,
        on_delete=models.CASCADE,
        related_name='data',
    )
    nr = models.FloatField(help_text='nível do reservatório')
    pzm = models.FloatField(help_text='piezômetro m')
    pzi = models.FloatField(help_text='piezômetro i')
    pzj = models.FloatField(help_text='piezômetro j')

    def __str__(self):
        return f"{self.bloco} | {self.data}"

    def get_absolute_url(self):
        return reverse('app:blocodata_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'dados de bloco'
        verbose_name_plural = 'dados de blocos'
        ordering = ('bloco', 'data')
        unique_together = ['data', 'bloco']

    @property
    def npr(self):
        return stab_eqs.npr(
            self.nr, self.bloco.cota_base_montante
        )

    @property
    def area_jq(self):
        return stab_eqs.area_jq(
            self.bloco.dist_xj, self.pzi, self.pzj
        )

    @property
    def area_jqx(self):
        return stab_eqs.area_jqx(
            self.bloco.dist_xj
        )

    @property
    def area_iq(self):
        return stab_eqs.area_iq(
            self.bloco.dist_xi, self.bloco.dist_xj, 
            self.pzi, self.pzm
        )

    @property
    def area_iqx(self):
        return stab_eqs.area_iqx(
            self.bloco.dist_xj, self.bloco.dist_xi
        )

    @property
    def area_mq(self):
        return stab_eqs.area_mq(
            self.bloco.dist_xm, self.bloco.dist_xi, self.npr, self.pzm
        )

    @property
    def area_mqx(self):
        return stab_eqs.area_mqx(
            self.bloco.dist_xi, self.bloco.dist_xm
        )

    @property
    def area_jt(self):
        return stab_eqs.area_jt(
            self.bloco.dist_xj, self.pzi, self.pzj
        )

    @property
    def area_jtx(self):
        return stab_eqs.area_jtx(
            self.pzi, self.pzj, self.bloco.dist_xj
        )

    @property
    def area_it(self):
        return stab_eqs.area_it(
            self.bloco.dist_xi, self.bloco.dist_xj, 
            self.pzm, self.pzi
        )

    @property
    def area_itx(self):
        return stab_eqs.area_itx(
            self.pzm, self.pzi, self.bloco.dist_xi, 
            self.bloco.dist_xj
        )

    @property
    def area_mt(self):
        return stab_eqs.area_mt(
            self.bloco.dist_xm, self.bloco.dist_xi,
            self.npr, self.pzm
        )

    @property
    def area_mtx(self):
        return stab_eqs.area_mtx(
            self.npr, self.pzm, 
            self.bloco.dist_xm, self.bloco.dist_xi
        )

    @property
    def area_total(self):
        return stab_eqs.area_total(
            self.area_jq, self.area_iq, self.area_mq, self.area_jt, 
            self.area_it, self.area_mt
        )

    @property
    def area_totalx(self):
        return stab_eqs.area_totalx(
            self.area_jq, self.area_jqx, self.area_iq, self.area_iqx,
            self.area_mq, self.area_mqx, self.area_jt, self.area_jtx, 
            self.area_it, self.area_itx, self.area_mt, self.area_mtx,
            self.area_total
        )

    @property
    def v_bloco(self):
        return stab_eqs.v_bloco(self.bloco.volume_bloco)

    @property
    def xcg_bloco(self):
        return stab_eqs.xcg_bloco(self.bloco.xcg_bloco)

    @property
    def v_enchimento(self):
        return stab_eqs.v_enchimento(
            self.bloco.v_enchimento
        )

    @property
    def xcg_enchimento(self):
        return stab_eqs.xcg_enchimento(
            self.bloco.xcg_enchimento
        )

    @property
    def v_agua(self):
        return stab_eqs.v_agua(
            self.nr, self.bloco.cota_ogiva,
            self.bloco.nr_vol_coeff.poly
        )

    @property
    def xcg_agua(self):
        return stab_eqs.xcg_agua(
            self.nr, self.bloco.cota_ogiva, 
            self.bloco.nr_xcg_coeff.poly
        )

    @property
    def v_sedimento(self):
        return stab_eqs.v_sedimento(
            self.bloco.cota_ogiva, self.bloco.cota_sedimento,
            self.bloco.largura
        )

    @property
    def xcg_sedimento(self):
        return stab_eqs.xcg_sedimento(
            self.bloco.cota_ogiva, self.bloco.cota_sedimento, 
            self.bloco.cota_base_jusante
        )

    @property
    def v_empuxo_agua1(self):
        return stab_eqs.v_empuxo_agua1(
            self.nr, self.pzm, c1=224.95, c2=1.6548, c3=28.125, c4=4.85,
            tipo_bloco=self.bloco.tipo, largura=self.bloco.largura
        )

    @property
    def v_empuxo_agua2(self):
        return stab_eqs.v_empuxo_agua2(
            self.nr, self.bloco.cota_base_montante, c1=18.35,
            tipo_bloco=self.bloco.tipo, largura=self.bloco.largura
        )

    @property
    def xcg_empuxo_agua1(self):
        return stab_eqs.xcg_empuxo_agua1(
            self.nr, self.pzm, c1=224.95, c2=28.125, c3=0.65903,
            c4=2.31, c5=2.5, c6=3.75, tipo_bloco=self.bloco.tipo
        )

    @property
    def xcg_empuxo_agua2(self):
        return stab_eqs.xcg_empuxo_agua2(
            self.nr, self.bloco.cota_base_montante,
            self.bloco.cota_base_jusante,
            tipo_bloco=self.bloco.tipo
        )

    @property
    def v_assoreamento(self):
        return stab_eqs.v_assoreamento(
            self.bloco.largura, self.bloco.cota_ogiva, self.bloco.cota_terreno
        )

    @property
    def xcg_assoreamento(self):
        return stab_eqs.xcg_assoreamento(
            self.bloco.cota_ogiva, self.bloco.cota_terreno,
            self.bloco.cota_base_jusante
        )

    @property
    def v_subpressao(self):
        return stab_eqs.v_subpressao(
            self.area_total, self.bloco.largura
        )

    @property
    def xcg_subpressao(self):
        return stab_eqs.xcg_subpressao(
            self.area_totalx
        )

    @property
    def fst(self):

        return stab_eqs.fst(
            self.v_bloco, self.xcg_bloco, self.bloco.gamma_concreto,
            self.v_enchimento, self.xcg_enchimento,
            self.bloco.gamma_enchimento, self.xcg_agua, self.v_agua,
            self.bloco.gamma_agua, self.v_sedimento, self.xcg_sedimento,
            self.bloco.gamma_sedimento, self.v_empuxo_agua1, 
            self.xcg_empuxo_agua1, self.v_empuxo_agua2, self.xcg_empuxo_agua2,
            self.v_assoreamento, self.bloco.angulo_sedimento,
            self.xcg_assoreamento, self.v_subpressao, self.xcg_subpressao
        )

    @property
    def fsd(self):
        return stab_eqs.fsd(
            self.v_bloco, self.bloco.gamma_concreto, self.v_enchimento, 
            self.bloco.gamma_enchimento, self.xcg_agua, self.bloco.gamma_agua,
            self.v_sedimento, self.bloco.gamma_sedimento, self.v_subpressao,
            self.bloco.phi, self.bloco.gamma_phi, self.bloco.c,
            self.bloco.area, self.bloco.gamma_c, self.v_empuxo_agua1,
            self.v_empuxo_agua2, self.v_assoreamento,
            self.bloco.angulo_sedimento
        )
