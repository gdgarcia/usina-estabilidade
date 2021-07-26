from django import forms

from app.models import Usina


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
