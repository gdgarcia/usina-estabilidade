from django.db import models

from app.models import Usina


class BundleData(models.Model):
    usina = models.ForeignKey(
        Usina,
        on_delete=models.CASCADE,
        related_name='bundle_data'
    )
    bundle_data = models.DateTimeField(db_index=True)
    already_converted_to_block_data = models.BooleanField(default=False)

    class Meta:
        unique_together = ['usina', 'bundle_data']
    
    def __str__(self):
        return f'{self.usina} | {self.bundle_data}'


class SensorData(models.Model):

    NIVEL_RESERVATORIO = 'nr'
    PIEZOMETRO = 'pz'
    SENSOR_DATA_CHOICES = [
        (None, 'Selecione o tipo do sensor...'),
        (NIVEL_RESERVATORIO, 'Nível do Reservatório'),
        (PIEZOMETRO, 'Medição do Piezômetro'),
    ]

    bundle_data = models.ForeignKey(
        BundleData,
        on_delete=models.CASCADE,
        related_name='sensor_data'
    )
    data = models.DateTimeField(db_index=True)
    type = models.CharField(
        max_length=2,
        choices=SENSOR_DATA_CHOICES,
        default=None,
    )
    number = models.IntegerField(blank=False, null=False, default=None)
    value = models.FloatField()

    class Meta:
        unique_together = ['bundle_data', 'type', 'number']

    def __str__(self):
        return f'{self.type} | {self.data} | {self.bundle_data}'
