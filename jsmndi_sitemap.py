import os
import xml.etree.ElementTree as ET
import requests

# Define a list to store the URLs
url_list = []

# Get the path to the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the file path where you want to save and check the URLs
output_file_path = os.path.join(script_dir, "sitemap_urls.txt")

# Read existing URLs from the output file (if it exists)
try:
    with open(output_file_path, "r") as file:
        url_list = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    pass

# Track the count of URLs before processing
urls_before_processing = len(url_list)

# List of sitemap URLs
sitemap_urls = [
    "https://jusmundi.com/sitemap-jusmundi.com-decision-en-1.xml",
    "https://jusmundi.com/sitemap-jusmundi.com-decision-en-2.xml",
    "https://jusmundi.com/sitemap-jusmundi.com-decision-en.xml"
]

# Loop through each sitemap URL
for sitemap_url in sitemap_urls:
    # Parse the XML data from the sitemap URL
    tree = ET.ElementTree(ET.fromstring(requests.get(sitemap_url).content))
    root = tree.getroot()

    # Find all <url> elements and extract the <loc> value
    for url_element in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        loc_element = url_element.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc_element is not None:
            url = loc_element.text.strip()
            
            # Check if the URL is not already in the list
            if url not in url_list:
                url_list.append(url)

# Write the extracted URLs to the output file
with open(output_file_path, "w") as file:
    for url in url_list:
        file.write(url + "\n")

# Calculate the count of additional URLs saved
urls_after_processing = len(url_list)
additional_urls_saved = urls_after_processing - urls_before_processing

# Print a message indicating the number of additional URLs saved
print(f"Extracted URLs have been saved to '{output_file_path}'")
print(f"Additional URLs saved: {additional_urls_saved}")
