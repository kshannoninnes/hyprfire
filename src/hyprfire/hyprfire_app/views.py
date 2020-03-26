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
