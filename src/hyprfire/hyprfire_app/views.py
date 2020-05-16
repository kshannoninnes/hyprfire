from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from hyprfire.settings import BASE_DIR
from hyprfire_app.forms import AnalyseForm
from hyprfire_app.CacheHandler import ScriptProcessor

from hyprfire_app.exceptions import JSONError
from hyprfire_app.new_scripts.kalon.packet_data_collector import PacketDataCollector
from hyprfire_app.new_scripts.kalon.packet_filter import PacketFilter
from hyprfire_app.new_scripts.kalon.pcap import write_packets_to_file, get_pcap_files_from
from hyprfire_app.new_scripts.kalon.timestamp import validate_timestamp
from hyprfire_app.new_scripts.kalon.validation import validate_file_path
from hyprfire_app.utils.json import validate_json_length, load_json

from tempfile import TemporaryFile

blacklist = [
    '.gitignore'
]


def index(request):
    filenames = get_pcap_files_from('pcaps')
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

        file_path = validate_file_path(f'{BASE_DIR}/pcaps/{data["filename"]}')
        start_timestamp = validate_timestamp(Decimal(data['start']))
        end_timestamp = validate_timestamp(Decimal(data['end']))

        pf = PacketFilter(file_path, start_timestamp, end_timestamp)
        packet_list = pf.get_filtered_list()

        with TemporaryFile() as file:
            write_packets_to_file(file, packet_list)
            response = HttpResponse(file)
            response['Content-Disposition'] = f'attachment; filename="{data["filename"]}-filtered.pcap"'

            return response

    # TODO Log the errors to make sure problems are traceable
    except JSONError as e:
        return HttpResponse(status=400, reason=e)
    except FileNotFoundError as e:
        return HttpResponse(status=404, reason=e)
    except Exception as e:
        return HttpResponse(status=500, reason='Something went wrong.')


def collect_packet_data(request):
    """
    collect_packet_data

    Endpoint: /collect/

    Collect specific packet details on all packets between two times

    Parameters
    request: An HTTP request provided by Django containing json in the POST body

    JSON Parameters
    filename: the file to collect a packet details from
    start: a unique seconds-based epoch timestamp to identify the first packet
    end: a unique seconds-based epoch timestamp to identify the last packet
    """
    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        data = load_json(request.body)
        validate_json_length(data, 3)

        file_path = validate_file_path(f'{BASE_DIR}/pcaps/{data["filename"]}')
        start_timestamp = validate_timestamp(Decimal(data['start']))
        end_timestamp = validate_timestamp(Decimal(data['end']))

        pf = PacketFilter(file_path, start_timestamp, end_timestamp)
        packet_list = pf.get_filtered_list()
        dc = PacketDataCollector(packet_list)
        packet_details = dc.get_details()

        return JsonResponse(data={'data': packet_details})

    except JSONError as e:
        return HttpResponse(status=400, reason=e)
    except FileNotFoundError as e:
        return HttpResponse(status=404, reason=e)
    except Exception as e:
        return HttpResponse(status=500, reason='Something went wrong.')
