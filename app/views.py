from dal import autocomplete
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import (
    UpdateView, CreateView, DeleteView 
)
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Usina, Bloco, BlocoData, NrVolCoeff, NrXcgCoeff
from .forms import (
    PlotSelectionForm,
    BlocoForm,
    NrVolCoeffForm,
    NrXcgCoeffForm
)
from .plotting import plot_figure


class HomeView(TemplateView):
    template_name = 'app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'home'
        context['plot_form'] = PlotSelectionForm()
        return context


class UsinaListView(ListView):
    model = Usina
    template_name = 'app/usina_list.html'
    context_object_name = 'all_usinas_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'usinas'
        return context


class UsinaDetailView(UpdateView):
    model = Usina
    template_name = 'app/usina_detail.html'
    fields = ['nome', 'descricao']

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['page'] = 'usinas'
        return context


class UsinaCreateView(CreateView):
    model = Usina
    template_name = 'app/usina_detail.html'
    fields = ['nome', 'descricao']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'usinas'
        return context


class UsinaDeleteView(DeleteView):
    model = Usina
    template_name = 'app/usina_delete.html'
    success_url = reverse_lazy('app:usina_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'usinas'
        return context


class UsinaDuplicateView(CreateView):
    model = Usina
    template_name = 'app/usina_detail.html'
    fields = ['nome', 'descricao']

    # need to to this. success url only as a class field cloud
    # not access object.pk
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'usinas'
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs['pk']
        usina = self.model.objects.get(pk=pk)
        initial.update({
            'nome': ' - '.join((usina.nome, 'COPIA')),
            'descricao': usina.descricao,
        })
        return initial
    
    def get_success_url(self):
        return reverse_lazy('app:usina_detail', kwargs={'pk': self.object.pk})


class BlocoListView(ListView):
    model = Bloco
    template_name = 'app/bloco_list.html'
    context_object_name = 'all_blocos_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocos'
        return context


class BlocoDetailView(TemplateView):
    template_name = 'app/bloco_detail.html'

    def get(self, request, pk):
        bloco = get_object_or_404(Bloco, pk=pk)
        nr_vol_coeff = get_object_or_404(NrVolCoeff, bloco=bloco)
        nr_xcg_coeff = get_object_or_404(NrXcgCoeff, bloco=bloco)
        bloco_form = BlocoForm(instance=bloco)
        nr_vol_coeff_form = NrVolCoeffForm(instance=nr_vol_coeff)
        nr_xcg_coeff_form = NrXcgCoeffForm(instance=nr_xcg_coeff)
        return render(request, self.template_name, {
            'bloco_form': bloco_form, 'nr_vol_coeff_form': nr_vol_coeff_form,
            'nr_xcg_coeff_form': nr_xcg_coeff_form, 'bloco': bloco,
            'page': 'blocos' 
        })
    
    def post(self, request, pk):
        bloco = get_object_or_404(Bloco, pk=pk)
        nr_vol_coeff = get_object_or_404(NrVolCoeff, bloco=bloco)
        nr_xcg_coeff = get_object_or_404(NrXcgCoeff, bloco=bloco)
        bloco_form = BlocoForm(request.POST, instance=bloco)
        nr_vol_coeff_form = NrVolCoeffForm(request.POST,
                                           instance=nr_vol_coeff)
        nr_xcg_coeff_form = NrXcgCoeffForm(request.POST,
                                           instance=nr_xcg_coeff)
        if (
            bloco_form.is_valid() and
            nr_vol_coeff_form.is_valid() and
            nr_xcg_coeff_form.is_valid()
        ):
            bloco_form.save()
            nr_vol = nr_vol_coeff_form.save(commit=False)
            nr_vol.bloco = bloco
            nr_vol.save()
            nr_xcg = nr_xcg_coeff_form.save(commit=False)
            nr_xcg.bloco = bloco
            nr_xcg.save()
            return redirect(bloco.get_absolute_url())
            
        else:
            return render(request, self.template_name,
                {'bloco_form': bloco_form,
                 'nr_vol_coeff_form': nr_vol_coeff_form,
                 'nr_xcg_coeff_form': nr_xcg_coeff_form, 'bloco': bloco,
                 'page': 'blocos'})


class BlocoCreateView(TemplateView):
    template_name = 'app/bloco_detail.html'

    def get(self, request):
        bloco_form = BlocoForm()
        nr_vol_coeff_form = NrVolCoeffForm()
        nr_xcg_coeff_form = NrXcgCoeffForm()
        bloco = Bloco.objects.none()
        return render(request, self.template_name,
                      {'bloco_form': bloco_form,
                       'nr_vol_coeff_form': nr_vol_coeff_form,
                       'nr_xcg_coeff_form': nr_xcg_coeff_form, 'bloco': bloco,
                       'page': 'blocos' })
    
    def post(self, request):
        bloco_form = BlocoForm(request.POST)
        nr_vol_coeff_form = NrVolCoeffForm(request.POST)
        nr_xcg_coeff_form = NrXcgCoeffForm(request.POST)
        if (
            bloco_form.is_valid() and
            nr_vol_coeff_form.is_valid() and
            nr_xcg_coeff_form.is_valid()
        ):
            bloco = bloco_form.save(commit=False)
            nr_vol = nr_vol_coeff_form.save(commit=False)
            nr_xcg = nr_xcg_coeff_form.save(commit=False)
            bloco.save()
            nr_vol.bloco = bloco
            nr_vol.save()
            nr_xcg.bloco = bloco
            nr_xcg.save()
            return redirect(bloco.get_absolute_url())
        else:
            bloco = Bloco.objects.none()
            return render(request, self.template_name,
                          {'bloco_form': bloco_form,
                           'nr_vol_coeff_form': nr_vol_coeff_form,
                           'nr_xcg_coeff_form': nr_xcg_coeff_form,
                           'bloco': bloco, 'page': 'blocos'})


class BlocoDeleteView(DeleteView):
    model = Bloco
    template_name = 'app/bloco_delete.html'
    success_url = reverse_lazy('app:bloco_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocos'
        return context


class BlocoDuplicateView(TemplateView):
    template_name = 'app/bloco_detail.html'

    def get(self, request, pk):
        bloco = get_object_or_404(Bloco, pk=pk)
        nr_vol_coeff = get_object_or_404(NrVolCoeff, bloco=bloco)
        nr_xcg_coeff = get_object_or_404(NrXcgCoeff, bloco=bloco)
        bloco.id = None
        bloco._state.adding = True
        nr_vol_coeff.bloco = None
        nr_vol_coeff._state.adding = True
        nr_xcg_coeff.bloco = None
        nr_xcg_coeff._state.adding = True
        bloco_form = BlocoForm(instance=bloco)
        nr_vol_coeff_form = NrVolCoeffForm(instance=nr_vol_coeff)
        nr_xcg_coeff_form = NrXcgCoeffForm(instance=nr_xcg_coeff)
        return render(request, self.template_name,
                {'bloco_form': bloco_form,
                 'nr_vol_coeff_form': nr_vol_coeff_form,
                 'nr_xcg_coeff_form': nr_xcg_coeff_form, 'bloco': bloco,
                 'page': 'blocos'})

    def post(self, request, pk):
        bloco_form = BlocoForm(request.POST)
        nr_vol_coeff_form = NrVolCoeffForm(request.POST)
        nr_xcg_coeff_form = NrXcgCoeffForm(request.POST)
        if (
            bloco_form.is_valid() and
            nr_vol_coeff_form.is_valid() and
            nr_xcg_coeff_form.is_valid()
        ):
            bloco = bloco_form.save(commit=False)
            nr_vol = nr_vol_coeff_form.save(commit=False)
            nr_xcg = nr_xcg_coeff_form.save(commit=False)
            bloco.save()
            nr_vol.bloco = bloco
            nr_vol.save()
            nr_xcg.bloco = bloco
            nr_xcg.save()
            return redirect(bloco.get_absolute_url())
        else:
            bloco = Bloco.objects.none()
            return render(request, self.template_name,
                          {'bloco_form': bloco_form,
                           'nr_vol_coeff_form': nr_vol_coeff_form,
                           'nr_xcg_coeff_form': nr_xcg_coeff_form,
                           'bloco': bloco, 'page': 'blocos'})


class BlocoDataListView(ListView):
    model = BlocoData
    template_name = 'app/blocodata_list.html'
    context_object_name = 'all_blocodata_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocodata'
        return context


class BlocoDataDetailView(UpdateView):
    model = BlocoData
    template_name = 'app/blocodata_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocodata'
        return context


class BlocoDataCreateView(CreateView):
    model = BlocoData
    template_name = 'app/blocodata_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocodata'
        return context


class BlocoDataDeleteView(DeleteView):
    model = BlocoData
    template_name = 'app/blocodata_delete.html'
    success_url = reverse_lazy('app:blocodata_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocodata'
        return context


class BlocoDataDuplicateView(CreateView):
    model = BlocoData
    template_name = 'app/blocodata_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocodata'
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs['pk']
        blocodata =  get_object_or_404(self.model, pk=pk)
        initial.update({
            'data': blocodata.data,
            'bloco': blocodata.bloco,
            'nr': blocodata.nr,
            'pzm': blocodata.pzm,
            'pzi': blocodata.pzi,
            'pzj': blocodata.pzj,
        })
        return initial

    def get_success_url(self):
        return reverse_lazy('app:blocodata_detail',
                            kwargs={'pk': self.object.pk})


class PlotBlocoDataView(TemplateView):
    template_name = 'app/blocodata_plot.html'

    def get(self, request):
        bokeh_div = None
        bokeh_script = None
        if self.request.GET.get('bloco'):
            plot_form = PlotSelectionForm(self.request.GET)
            if plot_form.is_valid():
                cd = plot_form.cleaned_data
                bloco = cd['bloco']
                data_initial = cd['data_initial']
                data_final = cd['data_final']
                attr = cd['tipo']

                blocodata_plot_list = BlocoData.objects.filter(
                    Q(bloco=bloco) &
                    Q(data__gte=data_initial) &
                    Q(data__lte=data_final)
                ).order_by('data')
                dados = [getattr(b, attr) for b in blocodata_plot_list]
                datas = [b.data for b in blocodata_plot_list]
                bokeh_script, bokeh_div = plot_figure(
                    datas, dados, "x - axis", "y - axis", "Title Teste"
                )
        else:
            plot_form = PlotSelectionForm()

        return render(request, self.template_name, 
                      {'page': 'plots',
                       'plot_form': plot_form,
                       'bokeh_script': bokeh_script,
                       'bokeh_div': bokeh_div})


class BlocoAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        usina = self.forwarded.get('usina', None)

        if usina:
            return Bloco.objects.filter(usina=usina).order_by('nome')
        else:
            return Bloco.objects.none()
