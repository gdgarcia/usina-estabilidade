from django.urls import path

from .views import (
    ChooseDataView,
    # ConfirmInsertionView,
    # DataConvertionView,
    data_uploaded_view,
) 

app_name = 'sensor_data'

urlpatterns = [
    path('load-data/', ChooseDataView.as_view(), name='load_data'),
    # path('confirm-insertion/', ConfirmInsertionView.as_view(),
    #      name='confirm_insertion'),
    # path('data-convert/', DataConvertionView.as_view(),
    #      name='data_convertion'),
    path('loaded-data/', data_uploaded_view, name='loaded_data'),
]
