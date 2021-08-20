from django import forms

from app.models import Usina
from .models import BundleData, SensorData


class FolderSelectionForm(forms.Form):
    COMMA_SEPARATOR = ','
    SEMICOLON_SEPARATOR = ';'
    DOT_SEPARATOR = '.'

    DATA_SEPARATOR_CHOICES_AUTO = [
        (COMMA_SEPARATOR, ','),
        (SEMICOLON_SEPARATOR, ';'), 
    ]

    DECIMAL_SEPARATOR_CHOICES_AUTO = [
        (DOT_SEPARATOR, '.'),
        (COMMA_SEPARATOR, ','),
    ]

    DATA_SEPARATOR_CHOICES_MAN = [
        (SEMICOLON_SEPARATOR, ';'),
        (COMMA_SEPARATOR, ','), 
    ]

    DECIMAL_SEPARATOR_CHOICES_MAN = [
        (COMMA_SEPARATOR, ','),
        (DOT_SEPARATOR, '.'),
    ]

    CSV_FILE = 'csv'

    EXTENSION_CHOICES = [
        (CSV_FILE, '.csv'),
    ]

    file = forms.FileField(
        label='Arquivo Zipado',
        help_text='Pasta zipada com os dados dos sensores',
    )

    usina = forms.ModelChoiceField(
        queryset=Usina.objects.all(),
        label='Usina',
        help_text='Usina a qual os dados pertencem',
        empty_label='Selecione a usina...'
    )

    extension = forms.ChoiceField(
        choices=EXTENSION_CHOICES,
        label='Extensão',
        help_text='Extensão dos arquivos a serem lidos.'
    )

    auto_data_marker = forms.CharField(
        max_length=10, initial='autom',
        label='Indicador dado automatizado',
        help_text='Parte do título do arquivo que indica ser medição'
                  ' automatizada',
    )
    auto_data_separator = forms.ChoiceField(
        choices=DATA_SEPARATOR_CHOICES_AUTO,
        label='Separador dados automatizados',
        help_text='Caracter que indica a separação de dados automatizados',
    )
    auto_decimal_separator = forms.ChoiceField(
        choices=DECIMAL_SEPARATOR_CHOICES_AUTO,
        label='Separador decimal automatizados',
        help_text='Caracter que indica a separação decimal nos automatizados',
    )
    man_data_separator = forms.ChoiceField(
        choices=DATA_SEPARATOR_CHOICES_MAN,
        label='Separador dados manuais',
        help_text='Caracter que indica a separação de dados manuais',
    )
    man_decimal_separator = forms.ChoiceField(
        choices=DECIMAL_SEPARATOR_CHOICES_MAN,
        label='Separador decimal manuais',
        help_text='Caracter que indica a separação decimal nos manuais',
    )


class BundleSaveForm(forms.Form):
    SALVAR = 'sv'
    SALVAR_E_ATUALIZAR = 'sva'
    NAO_SALVAR = 'd'

    SALVAR_DADOS_OPCOES = [
        (None, 'Selecione a opção...'),
        (SALVAR, 'Salvar'),
        (SALVAR_E_ATUALIZAR, 'Salvar e atualizar'),
        (NAO_SALVAR, 'Descartar'),
    ]

    salvar_dados = forms.ChoiceField(
        choices=SALVAR_DADOS_OPCOES,
        label='Opções para salvar dados',
        help_text='Salvar: salva dados novos e descarta os repetidos. Salvar '
        'e atualizar: salva os dados novos e atualiza os repetidos.',
    )


class BundleDataUpdateForm(forms.ModelForm):
    class Meta:
        model = BundleData
        fields = ['usina', 'bundle_data']
        labels = {'usina': 'Usina', 'bundle_data': 'Data'}
    
    def clean(self):
        fields = self.cleaned_data


BundleDataUpdateFormset = forms.inlineformset_factory(
    BundleData,
    SensorData,
    form=BundleDataUpdateForm,
    extra=0,
    can_delete=True,
    max_num=30,
    validate_max=30,
    fields = ('data', 'type', 'number', 'value'),
    labels = {'data': 'Data', 'type': 'Tipo do Sensor',
              'number': 'Número', 'value': 'Valor'}
)


class BundleConvertForm(forms.Form):
    usina = forms.ModelChoiceField(
        queryset=Usina.objects.all(),
        label='Usina',
        help_text='Usina cujos pacotes de sensores devem ser convertidos',
        empty_label='Selecione a usina...',
    )
    date_init = forms.DateField(
        label='Data Inicial',
        required=False,
        widget= forms.DateInput(attrs={'type': 'date'})
    )
    date_end = forms.DateField(
        label='Data Final',
        required=False,
        widget= forms.DateInput(attrs={'type': 'date'})
    )
    delete_bundles = forms.BooleanField(
        label='Deletar os pacotes?',
        help_text='Deleta os dados de sensores após serem convertidos',
        required=True,
        initial=True
    )

