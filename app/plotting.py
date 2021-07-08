from math import pi

from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter, HoverTool
from bokeh.embed import components


def plot_figure(x_data, y_data, x_label="", y_label="", title="", 
                width=900, height=600, str_format="%d %B %Y %H:%M",
                label_orientation=pi/4.):
    
    fig = figure(title=title, x_axis_type="datetime",
                 plot_width=width, plot_height=height,
                 tools='pan,box_zoom,wheel_zoom,save,reset')
    
    fig.title.align = 'center'

    fig.yaxis.formatter.use_scientific = False
    fig.yaxis.axis_label = y_label

    fig.xaxis.formatter = DatetimeTickFormatter(
        hours=str_format,
        days=str_format,
        months=str_format,
        years=str_format,
    )

    fig.xaxis.major_label_orientation = label_orientation

    hover_tool = HoverTool(
        tooltips=[
            (f'{x_label}', '@x{%Y-%m-%d %H:%M:%S}'),
            (f'{y_label}', '@y'),

        ],
        formatters={
            '@x': 'datetime',
        },
        mode='vline',
    )

    fig.tools.append(hover_tool)

    fig.line(x_data, y_data)
    fig.circle(x_data, y_data, size=2.)

    bokeh_script, bokeh_div = components(fig)

    return bokeh_script, bokeh_div
