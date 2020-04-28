from django.urls import path
from . import views
from .views import index
from hyprfire_app.ajax_handlers import get_graph

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:filename>/', get_graph, name='get_graph'),
]