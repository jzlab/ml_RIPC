from src.process_data import fetch_data,process_data

proj_root = '/home/elijahc/dev/ml_ripc'
rel_fn = 'ripc_rel.csv'
abs_fn = 'ripc_abs.xlsx'

# Fetch abs data
abs_fp = fetch_data(
        file_id='16mfxWNoziyAlKZT2TN94MXxF4PX8V1vC',
        filename=abs_fn
        )

# Fetch rel data
rel_fp = fetch_data(
        file_id='1Armttbral27bY8f55sAVfvIm1Vh8f3a9',
        filename=rel_fn
        )

# Process csv into dataframe
rel_df = process_data(rel_fp)
print(rel_df.head())
