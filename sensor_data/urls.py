from django.urls import path

from .views import (
    ChooseDataView,
    BundleDataListView,
    BundleDataDetailView,
    BundleDataDeleteView,
    BundleDataUpdateView,
    BundleDataConverterView,
    data_uploaded_view,
)

app_name = 'sensor_data'

urlpatterns = [
    path('load-data/', ChooseDataView.as_view(),
         name='load_data'),
    path('loaded-data/', data_uploaded_view,
         name='loaded_data'),
    path('bundle-list/', BundleDataListView.as_view(),
         name='bundle_list'),
    path('bundle-detail/<int:pk>/', BundleDataDetailView.as_view(),
         name='bundle_detail'),
    path('bundle-delete/<int:pk>/', BundleDataDeleteView.as_view(),
         name='bundle_delete'),
    path('bundle-update/<int:pk>/', BundleDataUpdateView.as_view(),
         name='bundle_update'),
    path('bundle-converter/', BundleDataConverterView.as_view(),
         name='bundle_converter'),
]
