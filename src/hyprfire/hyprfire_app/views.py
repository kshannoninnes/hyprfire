from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from hyprfire_app.forms import AnalyseForm
from pathlib import Path
from hyprfire_app.CacheHandler import ScriptProcessor

from hyprfire.settings import BASE_DIR

from hyprfire_app.exceptions import JSONError
from hyprfire_app.new_scripts.packet_manipulator.editcap import create_packet_list
from hyprfire_app.new_scripts.packet_manipulator.scapy import collect_packets, write_packets_to_file, get_packet_data
from hyprfire_app.new_scripts.packet_manipulator.timestamp import validate_timestamp
from hyprfire_app.utils.json import validate_json_length, load_json

from tempfile import TemporaryFile

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
    """
    download_pcap_snippet

    Endpoint: /download/

    Download a snippet of pcaps from a specific file

    Parameters
    request: An HTTP request provided by Django containing json in the POST body

    JSON Parameters
    filename: the file to collect a snippet from
    start: a unique seconds-based epoch timestamp to identify the first packet
    end: a unique seconds-based epoch timestamp to identify the last packet
    """

    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        data = load_json(request.body)
        validate_json_length(data, 3)

        file_path = Path(BASE_DIR) / 'pcaps' / data['filename']
        start_timestamp = Decimal(data['start'])
        end_timestamp = Decimal(data['end'])

        validate_timestamp(start_timestamp)
        validate_timestamp(end_timestamp)
        if not file_path.is_file():
            raise FileNotFoundError('File Not Found.')

        editcap_list = create_packet_list(file_path, start_timestamp, end_timestamp)
        packet_list = collect_packets(editcap_list, start_timestamp, end_timestamp)

        with TemporaryFile() as file:
            write_packets_to_file(file, packet_list)
            file.seek(0)
            response = HttpResponse(file)
            response['Content-Disposition'] = f'attachment; filename="{file_path.stem}-filtered.pcap"'

            return response

    # TODO Log the errors to make sure problems are traceable
    except JSONError as e:
        return HttpResponse(status=400, reason=e)
    except FileNotFoundError as e:
        return HttpResponse(status=404, reason=e)
    except Exception as e:
        return HttpResponse(status=500, reason='Something went wrong.')


def collect_packet_data(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        data = load_json(request.body)
        validate_json_length(data, 3)

        file_path = Path(BASE_DIR) / 'pcaps' / data['filename']
        start_timestamp = Decimal(data['start'])
        end_timestamp = Decimal(data['end'])

        validate_timestamp(start_timestamp)
        validate_timestamp(end_timestamp)
        if not file_path.is_file():
            raise FileNotFoundError('File Not Found.')

        editcap_list = create_packet_list(file_path, start_timestamp, end_timestamp)
        scapy_list = collect_packets(editcap_list, start_timestamp, end_timestamp)
        packet_data = {'data': get_packet_data(scapy_list)}

        return JsonResponse(data=packet_data)
    except JSONError as e:
        return HttpResponse(status=400, reason=e)
    except FileNotFoundError as e:
        return HttpResponse(status=404, reason=e)
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
