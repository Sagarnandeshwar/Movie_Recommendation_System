import os
from pathlib import Path

# removes all files in ../data folder
def cleanup_data_folder():
    [f.unlink() for f in Path("../data").glob("*") if f.is_file()] 