from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
     path('', views.HomeView.as_view(), name='home'),

     # usinas urls
     path('usinas/', views.UsinaListView.as_view(), name='usina_list'),
     path('usinas/create/', views.UsinaCreateView.as_view(),
          name='usina_create'),
     path('usina/<int:pk>/', views.UsinaDetailView.as_view(),
          name='usina_detail'),
     path('usina/<int:pk>/delete/', views.UsinaDeleteView.as_view(),
          name='usina_delete'),
     path('usina/<int:pk>/duplicate/', views.UsinaDuplicateView.as_view(),
          name='usina_duplicate'),

     # blocos urls
     path('blocos/', views.BlocoListView.as_view(), name='bloco_list'),
     path('blocos/create/', views.BlocoCreateView.as_view(),
          name='bloco_create'),
     path('bloco/<int:pk>/', views.BlocoDetailView.as_view(),
          name='bloco_detail'),
     path('bloco/<int:pk>/delete/', views.BlocoDeleteView.as_view(),
          name='bloco_delete'),
     path('bloco/<int:pk>/duplicate/', views.BlocoDuplicateView.as_view(),
          name='bloco_duplicate'),

     # blocodata urls
     path('blocodata/', views.BlocoDataListView.as_view(),
          name='blocodata_list'),
     path('blocodata/create/', views.BlocoDataCreateView.as_view(),
          name='blocodata_create'),
     path('blocodata/<int:pk>/', views.BlocoDataDetailView.as_view(),
          name='blocodata_detail'),
     path('blocodata/<int:pk>/delete/', views.BlocoDataDeleteView.as_view(),
          name='blocodata_delete'),
     path('blocodata/<int:pk>/duplicate/',
          views.BlocoDataDuplicateView.as_view(), name='blocodata_duplicate'),
     
     # url do plot de dados
     path('plot/', views.PlotBlocoDataView.as_view(), 
          name='plot_data'),

     # ajax urls
     path('ajax/carrega-blocos/', views.BlocoAutoComplete.as_view(),
          name='bloco-autocomplete'),
]
