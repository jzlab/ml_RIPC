import glob
from os.path import join, dirname

import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row,column
from bokeh.models import ColumnDataSource, Select, Span,Slider
from bokeh.palettes import Plasma256
from bokeh.transform import log_cmap
from quilt.data.elijahc import ripc.clustering as cdat

import bokeh.plotting as bp

def get_dataset(timepoint,df=None,selected=None):
    if df is not None:
        src = df
    else:
        src = getattr(cdat,cluster_select.value)
    out = src.query("min == {}".format(timepoint)).copy()
    out['log10p-value'] = -np.log10(out['p-value'].values)

    return ColumnDataSource(data=out)

def make_volcano_plot(source,title):
    p = bp.figure(tools="pan,wheel_zoom,reset,save",
                toolbar_location=None,
                x_range=(-6,6),y_range=(0,12))

    p.title.text = title


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

def make_cluster_plot(source,title):
    p = bp.figure(tools='pan,lasso_select,save,reset,wheel_zoom', x_range=(-100,100), y_range=(-100,100))
    p.hover.tooltips = [
        ("Molecular Weight", "@{Molecular_Weight}"),
    ]
    p.circle('dim_1','dim_2', line_color=mapper, color=mapper, size=5,source=source)
    p.title.text = title

    return p

def update(selected=None):
    timepoint = timepoints[timepoint_select.value]
    volc_plot.title.text = "Volcano plot @ {}min".format(timepoint)

    src = get_dataset(timepoint,selected=selected)
    source.data.update(src.data)

def tp_change(attrname, old, new):
    update()

def dataset_change(attrname, old, new):
    update()

def selection_change(attrname, old, new):
    selected = source.selected.indices

    data = tsne_df
    if selected:
        data = data.iloc[selected, :]
    update(selected)

files = list(vars(cdat)['_children'].keys())
cluster_select = Select(value=files[0],title='Dataset',options=files)
timepoint_select = Slider(
        start=0,end=9,value=4,step=1,
        title='Timepoint',
        )

# Load data
print('loaded dataset')

timepoints = [2,4,6,8,10,20,30,45,60]
timepoint = timepoints[4]

df = getattr(cdat,cluster_select.value)()

mapper = log_cmap(field_name='Molecular_Weight', palette=Plasma256 ,low=min(df['Molecular_Weight'].values) ,high=max(df['Molecular_Weight'].values))

source = get_dataset(timepoint,df)

# Make plots
volc_plot = make_volcano_plot(source, "Volcano plot for @ {}min".format(timepoint))
cluster_plot = make_cluster_plot(source, "Clustering")

# Register callback funcs
cluster_select.on_change('value', dataset_change)
timepoint_select.on_change('value', tp_change)
source.on_change('selected', selection_change)

plots = row(volc_plot,cluster_plot)
controls = row(timepoint_select,cluster_select)

curdoc().add_root(column(plots,controls))
curdoc().title = "Volcano"
