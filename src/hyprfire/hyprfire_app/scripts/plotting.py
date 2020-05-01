from plotly.offline import plot
import plotly.graph_objects as go

# Read filename / csv string (Ask Quang)
# get_xy changes? (needs to end with ret_thing = [] basically double array
# feed ret_thing array into plottify as xy

# Get the x and y locations from the supplied file
def get_xy(filename, xcol, ycol):
    ret_thing = []
    with open(filename) as file:
        for line in file:
            try:
                lin = line.split(",")
                x = float(lin[xcol])
                y = float(lin[ycol])
                a = (x, y)
                ret_thing.append(a)
            except ValueError:
                print("Oh no, a thing happened. Maybe " + lin[xcol] + " or " + lin[ycol] + " aren't numbers?")
    return ret_thing


# Plot the data from the supplied file
def plottify(filename, xcol, ycol):
    xy = get_xy(filename, xcol, ycol)
    x = [k[0] for k in xy]
    y = [k[1] for k in xy]
    fig = go.Figure()
    scatter = go.Scatter(x=x, y=y, mode='lines', opacity=0.8, marker_color='blue', )
    fig.add_trace(scatter)
    fig.update_layout(title=f"Anomaly graph for {filename}",
                      xaxis_title="Time Value (microseconds)", yaxis_title="U Value")

    return fig


# Get a plot using the data in the supplied file
# change filename to csv string
def get_plot(filename):
    plt = plottify(filename, 0, 1)
    return plot(plt, output_type='div')

