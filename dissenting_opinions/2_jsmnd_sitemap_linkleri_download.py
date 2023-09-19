import os
import requests
import time
import hashlib
import logging
import random
# Configure logging
logging.basicConfig(filename='download.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_and_save_file(url, output_dir, proxies=None, max_length=255):
    try:
        response = requests.get(url, proxies=proxies, timeout=10)

        if response.status_code == 200:
            # Handle filename (truncate and append hash if necessary)
            filename = url.split("/")[-1]
            if len(filename) > max_length:
                filename = filename[:max_length-10] + hashlib.md5(filename.encode()).hexdigest()[:10]

            filename = os.path.join(output_dir, filename)
            
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {url} as {filename}")
            logging.info(f"Downloaded: {url} as {filename}")
            return True

        else:
            print(f"Failed to download: {url} (status code: {response.status_code})")
            logging.error(f"Failed to download: {url} (status code: {response.status_code})")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        logging.error(f"Error downloading {url}: {e}")
        return False

# Input file containing the list of URLs
input_file = "jsmnd_sitemap_urls.txt"

# Output directory to save downloaded files
output_dir = "downloaded_files"

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read URLs from the input file
with open(input_file, "r") as file:
    urls = file.readlines()

# Rotating proxy settings
proxies = {
    "http": "http://onmnxabn-rotate:plqsus62kpat@p.webshare.io:80/",
    "https": "http://onmnxabn-rotate:plqsus62kpat@p.webshare.io:80/"
}

# Adding progress tracking
progress_file = "download_progress.txt"
if os.path.exists(progress_file):
    with open(progress_file, "r") as file:
        completed_urls = set(line.strip() for line in file)
else:
    completed_urls = set()

# Loop through the URLs and download them
for url in urls:
    url = url.strip()
    if url not in completed_urls:
        success = download_and_save_file(url, output_dir, proxies=proxies)
        if success:
            with open(progress_file, "a") as file:
                file.write(url + '\n')
            time.sleep(random.uniform(10, 40))  # Random delay between 20 and 40 seconds

print("Download process completed.")
logging.info("Download process completed.")
