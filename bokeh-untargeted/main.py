import glob
from os.path import join, dirname

import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row,column
from bokeh.models import ColumnDataSource, Select, Span,Slider,Range1d
from bokeh.palettes import Plasma256,Category10_5
from bokeh.transform import log_cmap,linear_cmap
from quilt.data.elijahc import ripc

import bokeh.plotting as bp

cdat = ripc.clustering

def get_attr_range(source,attr,margin=0.0):
    vals = source.data[attr]
    src_min = min(vals)
    src_max = max(vals)
    return (src_min*(1.0+margin),src_max*(1.0+margin))

def get_dataset(timepoint,df=None,selected=None):
    if df is not None:
        src = df
    else:
        src = getattr(cdat,cluster_select.value)()
    out = src.query("min == {}".format(timepoint)).copy()
    out['log10p-value'] = -np.log10(out['p-value'].values)
    if 'cluster_id' not in out.columns.values.tolist():
        out['cluster_id']=0

    columns = [
        'Molecular_Weight',
        'dim_1',
        'dim_2',
        'log10p-value',
        'log2fc_mean',
        'min',
        'cluster_id',
        'p-value']

    return ColumnDataSource(data=out[columns])

def make_volcano_plot(source,title):
    xr = get_attr_range(source,'log2fc_mean',margin=0.1)
    yr = get_attr_range(source,'log10p-value',margin=0.1)

    p = bp.figure(tools="pan,lasso_select,save,reset,wheel_zoom,hover",
                # toolbar_location=None,
                x_range=xr,y_range=(0,yr[1]))

    p.hover.tooltips = [
        ("Name","@Name"),
        ("Molecular Weight", "@{Molecular_Weight}"),
        ("Log2 Fold Change", "@log2fc_mean"),
        ('p-value', '@{p-value}')
    ]

    p.title.text = title


    p.circle("log2fc_mean", "log10p-value", line_color=mapper,color=mapper,size=5,source=source,name='volc_circle')
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
    xr = get_attr_range(source,'dim_1',margin=0.1)
    yr = get_attr_range(source,'dim_2',margin=0.1)

    TOOLS = 'pan,lasso_select,save,reset,wheel_zoom,hover'

    p = bp.figure(tools=TOOLS, x_range=xr, y_range=yr)

    p.hover.tooltips = [
        ("Molecular Weight", "@{Molecular_Weight}"),
        ("Group", "@cluster_id"),
    ]
    p.circle('dim_1','dim_2', line_color=mapper, color=mapper, size=5,source=source,name='cluster_circle')
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
    left,right = get_attr_range(source,'dim_1',0.1)
    bot,top = get_attr_range(source,'dim_2',0.1)

    cluster_plot.x_range.start = left
    cluster_plot.x_range.end = right
    cluster_plot.y_range.start = bot
    cluster_plot.y_range.end = top

def selection_change(attrname, old, new):
    selected = source.selected.indices

    data = tsne_df
    if selected:
        data = data.iloc[selected, :]
    update(selected)

def color_by_select_change(attrname, old, new):
    print(old,new)
    mapper = mappers[color_by_select.value]
    vglyph = volc_plot.select(name='volc_circle')[0].glyph
    cglyph = cluster_plot.select(name='cluster_circle')[0].glyph
    cglyph.update(fill_color=mapper,line_color=mapper)
    vglyph.update(fill_color=mapper,line_color=mapper)
    update()

files = list(vars(cdat)['_children'].keys())
cluster_select = Select(value=files[0],title='Dataset',options=files)
timepoint_select = Slider(
        start=0,end=9,value=4,step=1,
        title='Timepoint',
        )
color_by = ['Molecular_Weight','cluster_id']
color_by_select = Select(value=color_by[0],title='Color by:',options=color_by)

# Load data
print('loaded dataset')

timepoints = [2,4,6,8,10,20,30,45,60]
timepoint = timepoints[4]

df = getattr(cdat,cluster_select.value)()

mappers = {
    'Molecular_Weight':log_cmap(field_name='Molecular_Weight', palette=Plasma256 ,low=min(df['Molecular_Weight'].values) ,high=max(df['Molecular_Weight'].values)),
    'cluster_id':linear_cmap(field_name='cluster_id',palette=Category10_5,low=0,high=4)
}
mapper = mappers[color_by_select.value]

source = get_dataset(timepoint,df)

# Make plots
volc_plot = make_volcano_plot(source, "Volcano plot for @ {}min".format(timepoint))
cluster_plot = make_cluster_plot(source, "Clustering")

# Register callback funcs
cluster_select.on_change('value', dataset_change)
timepoint_select.on_change('value', tp_change)
source.on_change('selected', selection_change)
color_by_select.on_change('value',color_by_select_change)

plots = row(volc_plot,cluster_plot)
controls = row(timepoint_select,cluster_select,color_by_select)

curdoc().add_root(column(plots,controls))
curdoc().title = "Volcano"
