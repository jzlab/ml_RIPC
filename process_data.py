from google_drive_downloader import GoogleDriveDownloader as gdd

ripc_abs_fid = '16mfxWNoziyAlKZT2TN94MXxF4PX8V1vC'
ripc_rel_fid = '1Armttbral27bY8f55sAVfvIm1Vh8f3a9'

# Download abs file
gdd.download_file_from_google_drive(
        file_id=ripc_abs_fid,
        dest_path='./data/ripc_abs_quant.xlsx')

# Download rel file
gdd.download_file_from_google_drive(
        file_id=ripc_rel_fid,
        dest_path='./data/ripc_rel_quant.csv')
