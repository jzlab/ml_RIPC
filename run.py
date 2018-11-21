from src.process_data import fetch_data,process_data,load_data

proj_root = '/Users/elijahc/dev/ml_RIPC'
rel_fn = 'ripc_rel.csv'
abs_fn = 'ripc_abs.xlsx'

# Fetch abs data
abs_fp = fetch_data(
        file_id='16mfxWNoziyAlKZT2TN94MXxF4PX8V1vC',
        filename=abs_fn,
        proj_path=proj_root
        )

# Fetch rel data
rel_fp = fetch_data(
        file_id='1Armttbral27bY8f55sAVfvIm1Vh8f3a9',
        filename=rel_fn,
        proj_path=proj_root
        )

# Process csv into dataframe
# rel_df = process_data(rel_fp)
rel_df = load_data(rel_fp,proj_path=proj_root,normalize='log2_fc')
print(rel_df.head())
