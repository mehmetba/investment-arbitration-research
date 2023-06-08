import os
import pandas as pd
import re
import streamlit as st
from google.cloud import storage

# Create a Google Cloud Storage client
storage_client = storage.Client()

# Define the bucket name
bucket_name = "arbitration-text-search"  # Replace with your actual bucket name

# Function to search for keywords in a given text
def search_keywords(text, keywords):
    return any(keyword.lower() in text.lower() for keyword in keywords)

# Function to clean the text by removing line breaks and extra spaces
def clean_text(text):
    text = re.sub(r'\n', ' ', text)  # Remove line breaks
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text.strip()  # Remove leading/trailing spaces

def main():
    st.title("Keyword Search in Text Files")

    # Get the search keyword from the user
    keywords = st.text_input("Enter a search keyword:")
    keywords = [keywords] if keywords else []

    if st.button("Search"):
        # Create a new DataFrame to store the results
        results_df = pd.DataFrame(columns=['file_name', 'paragraph'])

        # Iterate through all files in the bucket
        bucket = storage_client.bucket(bucket_name)
        for blob in bucket.list_blobs():
            # Check if the file has a .txt extension
            if blob.name.endswith('.txt'):
                # Read the text file from the bucket
                content = blob.download_as_text()

                # Split the content into paragraphs
                paragraphs = content.split("\n\n")

                # Loop through the paragraphs
                for paragraph in paragraphs:
                    # Apply the search_keywords function to the paragraph
                    contains_keywords = search_keywords(paragraph, keywords)

                    # If the paragraph contains the keywords, add it to the results DataFrame
                    if contains_keywords:
                        # Clean the paragraph text by removing line breaks and extra spaces
                        paragraph = clean_text(paragraph)

                        # Remove the '.txt' extension from the file name
                        file_name_short = os.path.splitext(blob.name)[0]

                        # Add the file name (without the full path and without the extension) and the cleaned paragraph to a temporary DataFrame
                        temp_df = pd.DataFrame({'file_name': [file_name_short], 'paragraph': [paragraph]})

                        # Concatenate the temporary DataFrame with the results DataFrame
                        results_df = pd.concat([results_df, temp_df], ignore_index=True)

        # Drop duplicate paragraphs based on the 'paragraph' column
        results_df.drop_duplicates(subset='paragraph', inplace=True)

        if not results_df.empty:
            # Generate the Excel file name based on the search keyword
            excel_file_name = f"{keywords[0]}_search_results.xlsx"

            # Write the results DataFrame to an Excel file with the generated name
            results_df.to_excel(excel_file_name, index=False)
            st.success("Results generated successfully!")
            st.download_button(
                label="Download Results",
                data=excel_file_name,
                file_name=excel_file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.warning("No results found.")

if __name__ == '__main__':
    main()
