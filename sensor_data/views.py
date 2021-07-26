import os
import pickle

from tempfile import NamedTemporaryFile
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy

from .forms import FolderSelectionForm
from .read_data import read_data_from_folder
from .treat_data import aggregate_data


class ChooseDataView(FormView):
    template_name = 'sensor_data/data_selection.html'
    form_class = FolderSelectionForm
    success_url = reverse_lazy('sensor_data:loaded_data')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                folder_data = read_data_from_folder(cd['file'])
                out = aggregate_data(folder_data['data'])
                with NamedTemporaryFile(delete=False) as temp_file:
                    pickle.dump({'out': out, 'usina': cd['usina']},
                                open(temp_file.name, 'wb'))
                    temp_file.flush()
                    temp_file_name = temp_file.name
            except:
                # algum erro ocorreu. Temos de apagar a pasta temporaria
                # e levantar o erro novamente
                raise
            else:
                # somente queremos processar o redirect se nao houver erros 
                request.session['temp_file_name'] = temp_file_name
                return self.form_valid(form)
        # retornando o form com os erros eventuais e sem o arquivo na sessao
        return self.form_invalid(form)


def data_uploaded_view(request):
    usina = None
    dados = None
    campos = None
    if request.method == 'POST':
        pass
    else:
        try:
            temp_file_name = request.session['temp_file_name']

            with open(temp_file_name, 'rb') as fp:
                pickled = pickle.load(fp, encoding='utf-8')

            del request.session['temp_file_name']
            os.remove(temp_file_name)
        except (KeyError, FileNotFoundError):
            return redirect(reverse('sensor_data:load_data'))
        usina = pickled['usina']
        out = pickled['out'][0]
        for val in out.values():
            campos = list(val.keys())
            break
        campos.sort(key=lambda x: (x[:2], 0 if len(x)==2 else int(x[2:])))
        dados = []
        for key, val in out.items():
            dado = (val[campo] for campo in campos)
            dados.append(
                (key, *dado)
            )

    return render(request, 'sensor_data/data_presentation.html',
                    {'usina': usina, 'dados': dados, 'campos': campos})
