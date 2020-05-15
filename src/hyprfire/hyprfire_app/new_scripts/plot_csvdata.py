"""
File: plot_csvdata.py
Author: Quang Le
Purpose: use plotly library to convert list of csv data into a graph
"""

from plotly.offline import plot
import plotly.graph_objects as go


def get_csv_values(csvdata_list):
    """

    Description: Iterate over the list of csv values and extract them into a list of number arrays

    Parameter:
        csvdata_list (list): list of csv values

    Return:
        values (list): list of number arrays

    """
    values = []
    for row in csvdata_list:
        new = row.split(',')
        x = float(new[0])
        y = float(new[1])
        start = float(new[2])
        end = float(new[3])
        a = (x, y, start, end)
        values.append(a)
    return values


def get_plot(csvdata_list):
    """

    Description: takes in a list of csv values and convert it into a graph in a HTML div string format

    Parameter:
        csvdata_list (list): list of csv values

    Return:
        html_graph (str): a HTML div string which represents a graph of csvdata_list

    """
    if not isinstance(csvdata_list, list):
        print("Argument needs to be of a list type")
        raise TypeError(csvdata_list)
    csv_values = get_csv_values(csvdata_list)
    x_values = [row[0] for row in csv_values]
    y_values = [row[1] for row in csv_values]
    epoch_values = [(row[2], row[3]) for row in csv_values]
    fig = go.Figure()
    scatter = go.Scatter(x=x_values,
                         y=y_values,
                         customdata=epoch_values,
                         mode='lines',
                         opacity=0.8,
                         marker_color='blue')
    fig.add_trace(scatter)
    fig.update_layout(title="Anomaly graph",
                      xaxis_title="Time Value (microseconds)",
                      yaxis_title="U Value")
    fig.show()
    html_graph = plot(fig, output_type='div')
    return html_graph


