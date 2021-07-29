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
    path('loaded-data/', data_uploaded_view, name='loaded_data')
]
