from decimal import Decimal
from json.decoder import JSONDecodeError

from django.http import FileResponse, HttpResponse
from django.shortcuts import render

from hyprfire_app.forms import AnalyseForm
from pathlib import Path
from hyprfire_app.CacheHandler import ScriptProcessor

from hyprfire_app.new_scripts.packet_manipulator import packet_range_exporter
from hyprfire.settings import BASE_DIR
import json

from hyprfire_app.exceptions import PacketRangeExportError, JsonError

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
        data = load_json(request.body)
        file_path = str(Path(BASE_DIR) / 'pcaps' / data['filename'])
        start = data['start']
        end = data['end']

        output_path = packet_range_exporter.export_packets_in_range(file_path, start, end)
        file = open(output_path, 'rb')

        return FileResponse(file, as_attachment=True)

    # ESSENTIAL: Log the errors to make sure problems are traceable
    except PacketRangeExportError as e:
        return HttpResponse(status=400, reason=e)
    except JsonError as e:
        return HttpResponse(status=400, reason=e)
    except FileNotFoundError as e:
        return HttpResponse(status=404, reason='File Not Found.')
    except Exception as e:
        return HttpResponse(status=500, reason='Something went wrong.')


def load_json(request_body):
    try:
        data = json.loads(request_body)
    except JSONDecodeError:
        raise JsonError('Could not decode JSON.')

    if len(data) != 3:
        raise JsonError('Invalid parameters.')

    return data


def get_filenames():
    file_list = Path(monitored_dir).glob('*')
    filenames = []
    for path in file_list:
        name = path.stem.lower()
        if path.is_file() and name not in blacklist:
            filenames.append(name)

    return filenames
