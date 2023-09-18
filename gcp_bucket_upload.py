import os
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Check if the file already exists in the bucket
    if blob.exists():
        print(f"File {source_file_name} already exists in the bucket. Skipping upload.")
    else:
        blob.upload_from_filename(source_file_name)
        print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def upload_directory_to_bucket(bucket_name, directory_path):
    """Uploads a directory to the bucket."""
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            source_file_name = os.path.join(root, file_name)
            destination_blob_name = source_file_name.replace(directory_path + '/', "", 1)
            upload_blob(bucket_name, source_file_name, destination_blob_name)

bucket_name = "arbitration-text-search" # replace with your bucket name
directory_path = "/home/ubuntu/investment-arbitration-research/case_files"

upload_directory_to_bucket(bucket_name, directory_path)
