from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from hyprfire_app.forms import AnalyseForm
from pathlib import Path
from hyprfire_app.new_scripts.packet_manipulator import packet_range_exporter
from hyprfire.settings import BASE_DIR
from hyprfire_app.exceptions import PacketRangeExportError, JSONError
from hyprfire_app.utils.json import validate_json_length, load_json
from .CacheHandler import CacheHandler, ScriptProcessor


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

            #response = CacheHandler(filename, algorithm, window, analysis)
            response = ScriptProcessor(filename, algorithm, window, analysis)

            return render(request, 'hyprfire_app/index.html', {'form': form, 'filenames': filenames, 'graph': response})

    else:
        form = AnalyseForm()

    return render(request, 'hyprfire_app/index.html', {'form': form, 'filenames': filenames})


def download_pcap_snippet(request):
    """
    download_pcap_snippet

    Endpoint: /download/

    Download a snippet of pcaps from a specific file

    Parameters
    request: An HTTP request provided by Django

    Request Parameters
    filename: the file to collect a snippet from
    start: a unique seconds-based epoch timestamp to identify the first packet
    end: a unique seconds-based epoch timestamp to identify the last packet
    """

    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        data = load_json(request.body)
        validate_json_length(data, 3)

        file_path = str(Path(BASE_DIR) / 'pcaps' / data['filename'])
        start = data['start']
        end = data['end']

        output_path = packet_range_exporter.export_packets_in_range(file_path, start, end)
        file = open(output_path, 'rb')

        return FileResponse(file, as_attachment=True)

    # TODO Log the errors to make sure problems are traceable
    except PacketRangeExportError as e:
        return HttpResponse(status=400, reason=e)
    except JSONError as e:
        return HttpResponse(status=400, reason=e)
    except FileNotFoundError as e:
        return HttpResponse(status=404, reason='File Not Found.')
    except Exception as e:
        return HttpResponse(status=500, reason='Something went wrong.')


def get_filenames():
    file_list = Path(monitored_dir).glob('*')
    filenames = []
    for path in file_list:
        name = path.stem.lower()
        if path.is_file() and name not in blacklist:
            filenames.append(name)

    return filenames
