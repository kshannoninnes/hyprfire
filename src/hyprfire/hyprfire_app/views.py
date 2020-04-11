from django.views import generic
import os


class IndexView(generic.ListView):
    """ Load the initial view """

    template_name = 'hyprfire_app/index.html'

    def get_queryset(self):
        monitored_dir = 'pcaps'
        file_list = os.listdir(monitored_dir)
        filenames = []
        for file in file_list:
            name = file.title().lower()
            if name.endswith('.pcapng'):
                filenames.append(os.path.splitext(name)[0])
        return filenames
