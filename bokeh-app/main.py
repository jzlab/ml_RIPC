from os.path import join, dirname

import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row,column
from bokeh.models import ColumnDataSource, Select, Span
from bokeh.palettes import Plasma256
from bokeh.transform import log_cmap

import bokeh.plotting as bp


def get_dataset(src, timepoint):
    df = src.query("min == {}".format(timepoint)).copy()
    df['log10p-value'] = -np.log10(df['p-value'].values)
    # Implement any data munging here

    return ColumnDataSource(data=df)

def make_plot(source,title):
    p = bp.figure(tools="pan,wheel_zoom,reset,save",
                toolbar_location=None,
                x_range=(-6,6),y_range=(0,12))

    p.title.text = title

    mapper = log_cmap(field_name='Molecular_Weight', palette=Plasma256 ,low=min(df['Molecular_Weight'].values) ,high=max(df['Molecular_Weight'].values))

    p.circle("log2fc_mean", "log10p-value", line_color=mapper,color=mapper,size=5,source=source)
    p.xaxis.axis_label = "Log_2 Fold Change"
    p.yaxis.axis_label = "-log_10 p-value"
    p.axis.axis_label_text_font_style = "bold"

    sig_stat_line = Span(
            location=-np.log10(0.05),
            dimension='width',
            line_color='black',
            line_dash='dashed',
            line_width=1)

    p.add_layout(sig_stat_line)

    zero_change = Span(location=0,
            dimension='height',
            line_color='black',
            line_dash='dashed',
            line_width=1)
    p.add_layout(zero_change)

    return p

def update_plot(attrname, old, new):
    timepoint = timepoint_select.value
    plot.title.text = "Volcano plot for @ {}min".format(timepoint)

    src = get_dataset(df, timepoint)

    source.data.update(src.data)

timepoint = 2

timepoint_select = Select(value=str(timepoint),
        title='Timepoint',
        options=[str(t) for t in [2,4,6,8,10,20,30,45,60]]
        )

df = pd.read_pickle(join(dirname(__file__), 'ripc_fc.pk'))
print('loaded dataset')
source = get_dataset(df,timepoint)
plot = make_plot(source, "Volcano plot for @ {}min".format(timepoint))

timepoint_select.on_change('value', update_plot)

controls = column(timepoint_select)

curdoc().add_root(row(plot,controls))
curdoc().title = "Volcano"
