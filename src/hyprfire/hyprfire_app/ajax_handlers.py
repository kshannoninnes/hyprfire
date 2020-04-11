from django.http import HttpResponse
from hyprfire_app.scripts import plotting as plotting


def get_graph(request, filename):
    """ Retreive graph by filename """
    temp = plotting.get_plot(filename)
    return HttpResponse(temp, content_type='text/html')
