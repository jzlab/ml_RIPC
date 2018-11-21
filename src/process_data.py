import numpy as np
import pandas as pd
import os
import re

from google_drive_downloader import GoogleDriveDownloader as gdd

def fetch_data(file_id,filename,proj_path='/home/elijahc/dev/ml_ripc'):

    fp = os.path.join(proj_path,'data',filename)
    # Download abs file
    gdd.download_file_from_google_drive(
            file_id=file_id,
            dest_path=fp
            )

    return fp

def load_data(fn,proj_path='/home/elijahc/dev/ml_ripc'):
    fp = os.path.join(proj_path,fn)
    print('loading...'+fp)
    df = pd.read_csv(open(fp,mode='rb'),encoding='ISO-8859-1')

    return df


def process_data(fn,proj_path='/home/elijahc/dev/ml_ripc',normalize=None):
    df = load_data(fn,proj_path)

    print('')
    print('restructuring to longform...')
    print('(this may take a while)')

    cols = list(df.columns)

    rgx  = re.compile(r"(\d+)([A-L])")
    col_vec = list(filter(rgx.search,cols))

    if normalize is not None:
        baseline_rgx = re.compile(r"(\d+A)")
        t_rgx = lambda l: re.compile(r"(\d+{}).?".format(l))
        baseline = df[list(filter(baseline_rgx.search,cols))].as_matrix()
        final = [ df[list(filter(t_rgx(l).search,cols))].as_matrix() for l in col_vec ]

        if normalize=='log2_fc':
            norm_mat = [np.log2(f/baseline) for f in final]
        elif normalize=='fc':
            norm_mat = [f/baseline for f in final]

    long_df = pd.melt(df,id_vars=['Name','Formula','Molecular Weight'],value_vars=col_vec)
    pt_tp = list(long_df.variable)
    tp_mat = np.array(list(map(rgx.split,pt_tp)))[:,1:3]

    long_df['timepoint']=tp_mat[:,1]
    long_df['pt']=tp_mat[:,0]
    t_lookup = {k:v for k,v in zip(np.unique(tp_mat[:,1]),[0,0,2,4,6,8,10,20,30,45,60,60])}
    long_df['min']=[t_lookup[m] for m in list(long_df.timepoint)]
    # long_df['sec']=[t_lookup[m]*60 for m in list(long_df.timepoint)]

    return long_df
