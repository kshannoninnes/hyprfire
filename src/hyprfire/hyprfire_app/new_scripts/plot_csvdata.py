"""
File: plot_csvdata.py
Author: Quang Le
Purpose: use plotly to turn csvdata into a graph
"""

from plotly.offline import plot
import plotly.graph_objects as go
from hyprfire_app.new_scripts.packetdata_converter import CSVData


def get_csv_values(csvdata_list):
    values = []
    for row in csvdata_list:
        x = row.timestamp
        y = row.uvalue
        start = row.start_epoch
        end = row.end_epoch
        a = (x, y, start, end)
        values.append(a)
    return values


def get_plot(csvdata_list):
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


