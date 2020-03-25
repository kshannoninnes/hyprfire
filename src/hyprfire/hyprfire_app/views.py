from django.shortcuts import render
from os import listdir, path


def index(request):
    file_list = listdir()
    filenames = []
    for file in file_list:
        if file.title().lower().endswith('.pcapng'):
            filenames.append(file.title().lower())
    return render(request, 'hyprfire_app/index.html', {'files': filenames})
    # return render(request, 'hyprfire_app/index.html')
