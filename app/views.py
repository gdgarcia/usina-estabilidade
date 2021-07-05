from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import (
    UpdateView, CreateView, DeleteView 
)
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Usina, Bloco, BlocoData
from .forms import PlotSelectionForm
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


class BlocoDetailView(UpdateView):
    model = Bloco
    template_name = 'app/bloco_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocos'
        return context


class BlocoCreateView(CreateView):
    model = Bloco
    template_name = 'app/bloco_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocos'
        return context


class BlocoDeleteView(DeleteView):
    model = Bloco
    template_name = 'app/bloco_delete.html'
    success_url = reverse_lazy('app:bloco_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocos'
        return context


class BlocoDuplicateView(CreateView):
    model = Bloco
    template_name = 'app/bloco_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blocos'
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs['pk']
        bloco = self.model.objects.get(pk=pk)
        initial.update({
            'nome':  bloco.nome,
            'usina': bloco.usina,
            'volume_bloco': bloco.volume_bloco,
            'xcg_bloco': bloco.xcg_bloco,
            'largura': bloco.largura,
            'comprimento': bloco.comprimento,
            'area': bloco.area,
            'cota_base_montante': bloco.cota_base_montante,
            'cota_base_jusante': bloco.cota_base_jusante,
            'cota_ogiva': bloco.cota_ogiva,
            'cota_sedimento': bloco.cota_sedimento,
            'cota_terreno': bloco.cota_terreno,
            'v_enchimento': bloco.v_enchimento,
            'xcg_enchimento': bloco.xcg_enchimento,
            'dist_xm': bloco.dist_xm,
            'dist_xi': bloco.dist_xi,
            'dist_xj': bloco.dist_xj,
            'gamma_concreto': bloco.gamma_concreto,
            'gamma_agua': bloco.gamma_agua,
            'gamma_enchimento': bloco.gamma_enchimento,
            'gamma_sedimento': bloco.gamma_sedimento,
            'phi': bloco.phi,
            'c': bloco.c,
            'gamma_phi': bloco.gamma_phi,
            'gamma_c': bloco.gamma_c,
            'angulo_sedimento': bloco.angulo_sedimento,
        })
        return initial
    
    def get_success_url(self):
        return reverse_lazy('app:bloco_detail', kwargs={'pk': self.object.pk})


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
        blocodata = self.model.objects.get(pk=pk)
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


def carrega_blocos(request):
    usina_id = request.GET.get('usina')
    blocos = Bloco.objects.filter(usina=usina_id).order_by('nome')
    return render(request, 'app/home.html', {'blocos': blocos})
