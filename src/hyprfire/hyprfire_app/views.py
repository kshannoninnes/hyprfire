from django.http import FileResponse, HttpResponse
from django.shortcuts import render

from hyprfire_app.forms import AnalyseForm
from pathlib import Path
from hyprfire_app.CacheHandler import ScriptProcessor

from hyprfire_app.new_scripts.packet_manipulator import packet_range_exporter
from hyprfire.settings import BASE_DIR
import json

from hyprfire_app.new_scripts.exceptions import TimestampError, PacketsNotFoundError

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

            response = ScriptProcessor(filename, algorithm, window)

            return render(request, 'hyprfire_app/index.html', {'form': form, 'filenames': filenames, 'graph': response})

    else:
        form = AnalyseForm()

    return render(request, 'hyprfire_app/index.html', {'form': form, 'filenames': filenames})


def download_pcap_snippet(request):

    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return HttpResponse(status=400, reason='Could not decode JSON.')

    if len(data) != 3:
        return HttpResponse(status=400, reason='Invalid parameters.')

    try:
        file_path = Path(BASE_DIR) / 'pcaps' / data['file']
        output_path = packet_range_exporter.export_packets_in_range(str(file_path), data['start'], data['end'])
        file = open(output_path, 'rb')

        return FileResponse(file)

    except FileNotFoundError:
        return HttpResponse(status=404, reason='File Not Found.')
    except TimestampError:
        return HttpResponse(status=400, reason='Invalid timestamp.')
    except PacketsNotFoundError:
        return HttpResponse(status=400, reason='No packets found in range.')
    except Exception:
        # ESSENTIAL: Log the error to make sure problems are traceable
        return HttpResponse(status=500, reason='Something went wrong.')


def get_filenames():
    file_list = Path(monitored_dir).glob('*')
    filenames = []
    for path in file_list:
        name = path.stem.lower()
        if path.is_file() and name not in blacklist:
            filenames.append(name)

    return filenames
