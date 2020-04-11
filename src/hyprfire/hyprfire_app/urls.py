from django.urls import path
from .views import IndexView
from hyprfire_app.ajax_handlers import get_graph

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<slug:filename>/', get_graph, name='get_graph')
]