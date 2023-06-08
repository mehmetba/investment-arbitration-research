import os
import pandas as pd
import re

# Define the folder path
folder_path = "/home/ubuntu/investment-arbitration-research/case_files"

# Define the main keyword(s) you want to search for
keywords = ["investment-backed"]

# Function to search for keywords in a given text
def search_keywords(text):
    return any(keyword.lower() in text.lower() for keyword in keywords)

# Function to clean the text by removing line breaks and extra spaces
def clean_text(text):
    text = re.sub(r'\n', ' ', text)  # Remove line breaks
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text.strip()  # Remove leading/trailing spaces

# Create a new DataFrame to store the results
results_df = pd.DataFrame(columns=['file_name', 'paragraph'])

# Loop through all text files in the folder
for file_name in os.listdir(folder_path):
    # Check if the file has a .txt extension
    if file_name.endswith('.txt'):
        # Read the text file
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Split the content into paragraphs
        paragraphs = content.split("\n\n")
        
        # Loop through the paragraphs
        for paragraph in paragraphs:
            # Apply the search_keywords function to the paragraph
            contains_keywords = search_keywords(paragraph)
            
            # If the paragraph contains the keywords, add it to the results DataFrame
            if contains_keywords:
                # Clean the paragraph text by removing line breaks and extra spaces
                paragraph = clean_text(paragraph)
                
                # Remove the '.txt' extension from the file name
                file_name_short = os.path.splitext(file_name)[0]
                
                # Add the file name (without the full path and without the extension) and the cleaned paragraph to a temporary DataFrame
                temp_df = pd.DataFrame({'file_name': [file_name_short], 'paragraph': [paragraph]})
                
                # Concatenate the temporary DataFrame with the results DataFrame
                results_df = pd.concat([results_df, temp_df], ignore_index=True)

# Drop duplicate paragraphs based on the 'paragraph' column
results_df.drop_duplicates(subset='paragraph', inplace=True)

print(f"Keywords: {keywords}")

# Generate the CSV file name based on the search keyword
csv_file_name = f"/home/ubuntu/investment-arbitration-research/{keywords[0]}_search_results.csv"

# Write the results DataFrame to a CSV file with the generated name
results_df.to_csv(csv_file_name, index=False)
