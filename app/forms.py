from django import forms
from django.core.exceptions import ValidationError

from tempus_dominus.widgets import DateTimePicker

from .models import Usina, Bloco, NrVolCoeff, NrXcgCoeff


class PlotSelectionForm(forms.Form):
    usina = forms.ModelChoiceField(
        queryset=Usina.objects.all(),
        empty_label='Selecione a usina...',
    )
    bloco = forms.ModelChoiceField(
        # none. passaremos os valores via ajax apos usuario selecionar a usina
        # queryset=Bloco.objects.none(),  # para quando ajax ok
        queryset=Bloco.objects.all(),
        empty_label='Selecione o bloco...'
    )
    tipo = forms.ChoiceField(
        required=True,
        choices=(
            ('fsd', 'Fator FSD'), ('fst', 'Fator FST'),
        )
    )
    data_initial = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M']
    )
    data_final = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M']
    )

    def clean(self):
        """
        Validando que o bloco escolhido pertence a usina escolhida
        """
        cleaned_data = super().clean()
        usina = cleaned_data.get('usina')
        bloco = cleaned_data.get('bloco')

        if usina and bloco:
            if bloco.usina != usina:
                raise ValidationError(
                    f'O bloco {bloco.nome} nao pertence a usina {usina.nome}. '
                    f'Escolha a usina a que o bloco pertence.'
                )
        return cleaned_data



class BlocoForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = '__all__'


class NrVolCoeffForm(forms.ModelForm):
    class Meta:
        model = NrVolCoeff
        exclude = ['bloco']


class NrXcgCoeffForm(forms.ModelForm):
    class Meta:
        model = NrXcgCoeff
        exclude = ['bloco']
