import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import bokeh.plotting as bp
from bokeh.models import ColumnarDataSource, Span

def volcano_plot(volc_df,timepoint=2,xrange=(-4,4),yrange=(0,8),tools='pan,wheel_zoom,reset,hover,save',output_path=None):
    source = ColumnDataSource(volc_df.query('min == '+str(timepoint)))
    p = bp.figure(tools=tools, x_range=xrange, y_range=yrange)
    p.hover.tooltips = [
        ("Name","@Name"),
        ("Molecular Weight", "@{Molecular_Weight}"),
        ("Log2 Fold Change", "@log2fc_mean"),
        ('p-value', '@{p-value}')
    ]
    p.circle("log2fc_mean","log10p-value", size=5,source=source)

    p.title.text = "Population Volcano plot @ {}min".format(timepoint)
    p.yaxis.axis_label = '-log10(p-value)'
    p.xaxis.axis_label = 'log2(FoldChange)'


    sig_stat_line = Span(location=-np.log10(0.05),
                            dimension='width', line_color='black',
                            line_dash='dashed', line_width=1)
    p.add_layout(sig_stat_line)

    zero_change = Span(location=0,
                            dimension='height', line_color='black',
                            line_dash='dashed', line_width=1)
    p.add_layout(zero_change)
    
    if output_path is not None:
        bp.output_file(os.path.join(output_path,"volcano{}.html".format(timepoint)), title="Log2 Fold Change @ {}min".format(timepoint))

    return p

def pair_timeseries():
    