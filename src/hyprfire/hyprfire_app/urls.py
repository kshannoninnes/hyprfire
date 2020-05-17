from django.urls import path
from . import views

# TODO delete the below modules
from hyprfire_app.ajax_handlers import get_graph

urlpatterns = [
    path('', views.index, name='index'),
    path('download/<slug:filename>/<str:start>/<str:end>/', views.download_pcap_snippet, name='download_pcap_snippet'),
    path('collect/<slug:filename>/<str:start>/<str:end>/', views.collect_packet_data, name='collect_packet_data')
]