from django.shortcuts import render
from django.views import generic
from .forms import AnalyseForm
import os

monitored_dir = 'pcaps'
blacklist = [
    '.gitignore'
]


class IndexView(generic.ListView):
    """ Load the initial view """

    template_name = 'hyprfire_app/index.html'

    def get_queryset(self):
        file_list = os.listdir(monitored_dir)
        filenames = []
        for file in file_list:
            name = file.title().lower()
            if name not in blacklist:
                filenames.append(os.path.splitext(name)[0])
        return filenames


def analyse(request):
    if request.method == "POST":
        form = AnalyseForm(request.POST)
        if form.is_valid():
            window = form.cleaned_data['window']
            algorithm = form.cleaned_data['algorithm']
            length = form.cleaned_data['length']
    else:
        form = AnalyseForm()
    return render(request, 'hyprfire_app/index.html', {'form': form})
