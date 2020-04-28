from django.shortcuts import render
#from django.views import generic
from .forms import AnalyseForm
import os
from .CacheHandler import ScriptProcessor
from django.http import HttpResponse

monitored_dir = 'pcaps'
blacklist = [
    '.gitignore'
]


def index(request):
    filenames = get_filenames()
    if request.method == "POST":
        form = AnalyseForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data['filenames']
            window = form.cleaned_data['window']
            algorithm = form.cleaned_data['algorithm']
            length = form.cleaned_data['length']

            response = ScriptProcessor(algorithm, window)
            #print(response)

            return HttpResponse(response, content_type='text/html')

    else:
        form = AnalyseForm()

    return render(request, 'hyprfire_app/index.html', {'form': form, 'filenames': filenames})


def get_filenames():
    file_list = os.listdir(monitored_dir)
    filenames = []
    for file in file_list:
        name = file.title().lower()
        if name not in blacklist:
            filenames.append(os.path.splitext(name)[0])

    return filenames