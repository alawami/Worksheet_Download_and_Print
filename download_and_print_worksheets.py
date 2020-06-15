import requests
import time
import os
import subprocess

files_path = 'worksheets'

if not os.path.isdir(files_path):
    os.makedirs(files_path)

parts = list('abcdef')
extension = '.pdf'

def download_and_save_worksheet(url, path=''):
    try:
        response = requests.get(url)
        file_name = url.split('/')[-1]
        
        response.raise_for_status()
        
#         if response.status_code == 404:
#             print('File not found: ' + file_name)
#             return None
        
        with open(os.path.join(path, file_name), 'wb') as file:
            file.write(response.content)
            
        return file_name
            
    except requests.exceptions.HTTPError as error:
        print('File not found: ' + file_name)
        print(error)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Unexpected error", err)

def print_files(file, printer, options):
    pass

# Create list of potential urls
urls = []

with open('worksheet_url_prefix', 'r') as file:
    for urlprefix in file.readlines():
        # Drop newline character
        urls.extend([urlprefix[:-1] + part + extension for part in parts])

        
# Loop throught the urls
file_names = []

for url in urls:
    file_name = download_and_save_worksheet(url, files_path)
    
    if file_name is not None:
        file_names.append(file_name)
        
    time.sleep(0.100)
    
file_paths = [os.path.join(files_path, file_name) for file_name in file_names]


# Send files to the printer
for file in file_paths:
    print('Printing ' + file)
    subprocess.run(["lp", "-d", printer, "-o", "page-ranges=1", "-o", "fit-to-page", file])
    time.sleep(1)