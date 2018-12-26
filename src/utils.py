import os

def validate_cache(cache_path):
    file_status = cache_path is not None and isinstance(cache_path,str) and os.path.isfile(cache_path)
    
    return file_status