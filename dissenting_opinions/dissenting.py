import os

directory = '/home/ubuntu/gpt_openai/jusmuni_html_files'
keyword = 'dissent'
count = 0

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.lower().endswith('.html') and keyword in file.lower():
            print(os.path.join(root, file))
            count += 1

print(f"Number of files containing '{keyword}': {count}")
