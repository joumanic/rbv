import requests
import logging
import json
import os
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError



# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_folder(folderPath:str):
    url = "https://api.dropboxapi.com/2/files/list_folder"
    headers = {
    "Authorization": "Bearer " + os.getenv('DROPBOX_TOKEN'),
    "Content-Type": "application/json"
    }

    data = {
        "path": folderPath
    }

    try:
        logger.info("Sending List Folder request to Dropbox API")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raises an HTTPError for bad responses
        logger.info("Request sucessful.")
        return response.json()
    except HTTPError as httpErr:
        logger.error(f"HTTP error ocurred: {httpErr}")
    except Timeout as timeoutErr:
        logger.error(f"Request timed out: {timeoutErr}")
    except ConnectionError as connErr:
        logger.error(f"Connection error occured: {connErr}")
    except RequestException as reqErr:
        logger.error(f"An error ocurred: {reqErr}")
    except Exception as err:
        logger.error(f"An unexpected error ocurred: {err}")
    
    return None

def download_file(filePath:str):
    url = "https://content.dropboxapi.com/2/files/download"
    headers = {
        "Authorization": "Bearer " + os.getenv('DROPBOX_TOKEN'),    
        "Dropbox-API-Arg": f'{{"path": "{filePath}"}}'
}
    try:
        logger.info("Sending Download request to Dropbox API")
        response = requests.post(url, headers=headers)
        response.raise_for_status() # Raises an HTTPError for bad responses
        logger.info("Request sucessful.")
        return response
    except HTTPError as httpErr:
        logger.error(f"HTTP error ocurred: {httpErr}")
    except Timeout as timeoutErr:
        logger.error(f"Request timed out: {timeoutErr}")
    except ConnectionError as connErr:
        logger.error(f"Connection error occured: {connErr}")
    except RequestException as reqErr:
        logger.error(f"An error ocurred: {reqErr}")
    except Exception as err:
        logger.error(f"An unexpected error ocurred: {err}")
    
    return None

def upload_file(path:str,data:bytes):
    url = "https://content.dropboxapi.com/2/files/upload"
    headers = {
        "Authorization": "Bearer " + os.getenv('DROPBOX_TOKEN'), 
        "Content-Type": "application/octet-stream",   
        "Dropbox-API-Arg": f'{{"path": "{path}"}}'
        }
    
    try:
        logger.info("Sending Upload request to Dropbox API")
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status() # Raises an HTTPError for bad responses
        logger.info("Request sucessful.")
        return response
    except HTTPError as httpErr:
        logger.error(f"HTTP error ocurred: {httpErr}")
    except Timeout as timeoutErr:
        logger.error(f"Request timed out: {timeoutErr}")
    except ConnectionError as connErr:
        logger.error(f"Connection error occured: {connErr}")
    except RequestException as reqErr:
        logger.error(f"An error ocurred: {reqErr}")
    except Exception as err:
        logger.error(f"An unexpected error ocurred: {err}")
    
    return None 


if __name__ == '__main__':
    resp = get_folder(folderPath="/File requests/Images TEST")
    file = download_file(filePath=resp['entries'][0]['path_lower'])
    print(resp)