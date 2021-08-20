import os
import pickle

from tempfile import NamedTemporaryFile
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    FormView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse, reverse_lazy

from .models import BundleData
from .forms import (
    FolderSelectionForm, BundleSaveForm,
    BundleDataUpdateForm, BundleDataUpdateFormset
)
from .read_data import read_data_from_folder
from .treat_data import aggregate_data
from .bundles import save_bundle


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
    """
    View para apresentar e salvar os dados subidos.
    """
    # Tentando acessar o arquivo temporario com os dados.
    # Caso nao seja possivel, retornar a vista de carregamento dos dados.
    try:
        temp_file_name = request.session['temp_file_name']

        with open(temp_file_name, 'rb') as fp:
            pickled = pickle.load(fp, encoding='utf-8')

    except KeyError:
        return redirect(reverse('sensor_data:load_data'))
    except FileNotFoundError:
        try:
            del request.session['temp_file_name']
            os.remove(temp_file_name)
        except:
            pass
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

    if request.method == 'POST':
        save_form = BundleSaveForm(request.POST)
        if save_form.is_valid():
            salvar_dados = save_form.cleaned_data['salvar_dados']
            if salvar_dados == 'sv':
                created, updated = save_bundle(out, campos, usina,
                                               update=False)
                discarded = False
            elif salvar_dados == 'sva':
                created, updated = save_bundle(out, campos, usina,
                                               update=True)
                discarded = False
            else:
                # opcao de descartar os dados foi selecionada.
                # nao fazemos nada e apagamos o temp_file_name
                created, updated = 0, 0
                discarded = True

            del request.session['temp_file_name']
            os.remove(temp_file_name)

            return render(request, 'sensor_data/load_success.html',
                          {'discarded': discarded, 'created': created,
                           'updated': updated})
    else:
        save_form = BundleSaveForm()

    return render(request, 'sensor_data/data_presentation.html',
                  {'usina': usina, 'dados': dados, 'campos': campos,
                   'save_form': save_form})


class BundleDataListView(ListView):
    model = BundleData
    template_name = 'sensor_data/bundledata_list.html'
    paginate_by=50


class BundleDataDetailView(DetailView):
    model = BundleData
    template_name = 'sensor_data/bundledata_detail.html'
    context_object_name = 'bundle_data'


class BundleDataDeleteView(DeleteView):
    model = BundleData
    context_object_name = 'bundle_data'
    template_name = 'sensor_data/bundledata_delete.html'
    success_url = reverse_lazy('sensor_data:bundle_list')



class BundleDataUpdateView(UpdateView):
    template_name = 'sensor_data/bundledata_update.html'
    form_class = BundleDataUpdateForm
    model = BundleData
    success_message = 'Pacote de dados atualizado com sucesso'

    def get_success_url(self):
        return reverse_lazy('sensor_data:bundle_update',
                            kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(BundleDataUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = BundleDataUpdateForm(self.request.POST,
                                                   self.object)
            context['formset'] = BundleDataUpdateFormset(
                self.request.POST, isinstance=self.object
            )
        else:
            context['form'] = BundleDataUpdateForm(instance=self.object)
            context['formset'] = BundleDataUpdateFormset(instance=self.object)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = BundleDataUpdateFormset(self.request.POST,
                                          instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.get_success_url())
    
    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(
            form=form, formset=formset
        ))


def bundle_converter_view(request):
    return HttpResponse("Sensor Data Converter. Só um teste.")
