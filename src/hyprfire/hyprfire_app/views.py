import hyprfire_app.scripts.plotting as plotting

from django.http import FileResponse, HttpResponse, JsonResponse
from django.views import generic
from os import listdir


class IndexView(generic.ListView):
    template_name = 'hyprfire_app/index.html'

    def get_queryset(self):
        file_list = listdir()
        filenames = []
        for file in file_list:
            name = file.title().lower()
            if name.endswith('.pcapng'):
                filenames.append(name)
        return filenames


def send_image(request, slug):
    temp = plotting.get_plot('C:\\Users\\Mav\\PycharmProjects\\src\\2020-23-stefan-cyber\\src\hyprfire\\hyprfire_app\\scripts\\dump121.tcpd.n2d_benf_time.csv')
    return HttpResponse(temp, content_type='text/html')
