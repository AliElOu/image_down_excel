import pandas as pd
import os
from datetime import datetime
import time
import os
import requests


def download_image(image_url):
    if is_local_file(image_url):
        raise Exception(f"{date_now()} --> ✓ Image déja telechargé.")
    try:
        response = requests.get(image_url, stream=True)
    except:
        raise Exception(f"{date_now()} --> X Impossible de télécharger l'image.")
    if response.status_code == 200:
        image_name = os.path.basename(image_url.split('?')[0])  
        full_path = os.path.join("C:\\Users\\ali_e\\OneDrive\\Bureau\\images", image_name)
        with open(full_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return full_path
    else:
        raise Exception(f"{date_now()} --> X Impossible de télécharger l'image.")


def date_now():
    return datetime.now().strftime("%d/%m/%Y|%H:%M")


    
def is_local_file(path):
    return os.path.exists(path) and os.path.isfile(path)