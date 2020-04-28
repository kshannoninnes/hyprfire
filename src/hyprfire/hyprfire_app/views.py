from django.shortcuts import render
from django.views import generic
from .forms import AnalyseForm
import os

monitored_dir = 'pcaps'
blacklist = [
    '.gitignore'
]


def index(request):
    if request.method == "POST":
        form = AnalyseForm(request.POST)
        if form.is_valid():
            window = form.cleaned_data['window']
            algorithm = form.cleaned_data['algorithm']
            length = form.cleaned_data['length']
    else:
        form = AnalyseForm()
        file_list = os.listdir(monitored_dir)
        filenames = []
        for file in file_list:
            name = file.title().lower()
            if name not in blacklist:
                filenames.append(os.path.splitext(name)[0])
    return render(request, 'hyprfire_app/index.html', {'form': form, 'filenames': filenames})

