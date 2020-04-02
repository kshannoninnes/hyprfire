import base64

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
    name = f"{slug}-graph.svg"
    with open(f'hyprfire_app/static/hyprfire_app/{name}', 'rb') as f:
        return HttpResponse(f.read(), content_type="image/svg+xml")
