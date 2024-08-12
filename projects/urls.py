from django.urls import path
from django.contrib import admin
from .views import fetch_all_details, fetch_by_station, fetch_by_category, fetch_overall_info, fetch_overall_consumption
from .views import fetch_by_feeder, fetch_by_options, fetch_station_by_dtr, fetch_by_all_dtr
from .views import fetch_by_dtr, fetch_by_dtr_by_station, fetch_by_HT, fetch_by_HT_ID, insert_overall_details
from .views import fetch_overall_consumption

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/details/', fetch_all_details, name='fetch_all'),
    path('api/station-names/', fetch_by_station, name='fetch_by_station'),
    path('api/feeder-names/<str:station_name>/', fetch_by_feeder, name='fetch_by_feeder'),
    path('api/details/<str:station>/', fetch_by_category, name='fetch_by_category'),
    path('api/results/<str:st_name>/<str:fd_name>/', fetch_by_options, name='fetch_by_options'),
    path('api/station-dtr/<str:sname>/', fetch_station_by_dtr, name='fetch_station_by_dtr'),
    path('api/dtr/', fetch_by_all_dtr, name='fetch_all_by_dtr'),
    path('api/dtr/<str:station>/', fetch_by_dtr, name='fetch_by_dtr'),
    path('api/dtr-details/<str:dtr_id>/', fetch_by_dtr_by_station,
         name='fetch_by_dtr_by_station'),
    path('api/fetch-ht/', fetch_by_HT, name='fetch_by_HT'),
    path('api/fetch-htinfo/<str:consumer_id>/', fetch_by_HT_ID, name='fetch_by_HT'),
    path('api/fetch-overall/', fetch_overall_info, name='fetch_overall_info'),
    path('api/insert-overall-details/', insert_overall_details, name='insert-overall-details'),
    path('api/fetch-consumption/<int:feeder_code>/<str:date>/',fetch_overall_consumption,name='fetch_overall_consumption'),
]








