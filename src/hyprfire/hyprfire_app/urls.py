from django.urls import path
from .views import IndexView
from .CacheHandler import ScriptProcessor

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('<slug:filename>/', ScriptProcessor, name='ScriptProcessor')
]