"""
File: plot_csvdata.py
Author: Quang Le
Purpose: use plotly library to convert list of csv data into a graph
"""

from plotly.offline import plot
import plotly.graph_objects as go
import logging

logger = logging.getLogger(__name__)


def get_csv_values(csvdata_list):
    """

    Description: Iterate over the list of csv values and extract them into a list of number arrays

    Parameter:
        csvdata_list (list): list of csv values

    Return:
        values (list): list of number arrays

    """
    logger.info("Getting values from csvdata_list")
    values = []
    try:
        for row in csvdata_list:
            new = row.split(',')
            x = float(new[0])
            y = float(new[1])
            start = str(new[2])
            end = str(new[3])
            a = (x, y, start, end)
            values.append(a)
    except IndexError:
        raise IndexError("Index is out of range")
        logger.error("IndexError")
    return values


def get_plot(csvdata_list):
    """

    Description: takes in a list of csv values and convert it into a graph in HTML div string format which will be
    passed to the front-end for display

    Parameter:
        csvdata_list (list): list of csv values

    Return:
        html_graph (str): a HTML div string which represents a graph of csvdata_list

    """
    logger.info("Starting plot_csvdata...")
    #checks csvdata_list is valid
    if isinstance(csvdata_list, list):
        if len(csvdata_list) == 0:
            raise ValueError("List supplied is empty")
    else:
        raise TypeError("Argument needs to be of a list type")

    csv_values = get_csv_values(csvdata_list)

    logger.info("Plotting csv values..")
    x_values = [row[0] for row in csv_values]
    y_values = [row[1] for row in csv_values]
    epoch_values = [(row[2], row[3]) for row in csv_values]
    fig = go.Figure()
    scatter = go.Scatter(x=x_values,
                         y=y_values,
                         customdata=epoch_values,
                         mode='lines+markers',
                         opacity=0.8,
                         marker_color='blue')
    fig.add_trace(scatter)
    fig.update_layout(title="Anomaly graph",
                      xaxis_title="Time Value (microseconds)",
                      yaxis_title="U Value")
    html_graph = plot(fig, output_type='div')
    logger.info("Returning html div string for graph")

    return html_graph


