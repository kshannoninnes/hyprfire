from django.shortcuts import render

from .forms import AnalyseForm
from pathlib import Path
from .CacheHandler import CacheHandler

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
            analysis = form.cleaned_data['analysis']

            response = CacheHandler(filename, algorithm, window, analysis)

            return render(request, 'hyprfire_app/index.html', {'form': form, 'filenames': filenames, 'graph': response})

    else:
        form = AnalyseForm()

    return render(request, 'hyprfire_app/index.html', {'form': form, 'filenames': filenames})


def get_filenames():
    file_list = Path(monitored_dir).glob('*')
    filenames = []
    for path in file_list:
        name = path.stem.lower()
        if path.is_file() and name not in blacklist:
            filenames.append(name)

    return filenames
