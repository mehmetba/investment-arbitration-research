from bs4 import BeautifulSoup
import pandas as pd
import os

# Function to extract documents, arbitrators, and case name
def process_html_file(html_file_path):
    documents = []
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract case name
    case_name_div = soup.find('div', {'id': 'generalSubTitle'})
    case_name = case_name_div.get_text(strip=True) if case_name_div else None

    # Extract arbitrators
    arbitrators = []
    arbitrator_table = soup.find('table', {'class': 'metadata-group_table--arbitrator'})
    if arbitrator_table:
        for row in arbitrator_table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) == 2:
                name_link = columns[0].find('a')
                name = name_link.get_text(strip=True) if name_link else None
                status = columns[1].get_text(strip=True) if columns[1] else None
                arbitrators.append((name, status))

    # Function to extract documents
    def extract_documents(element, documents):
        for li in element.find_all('li', class_='listofdoc-level'):
            link = li.find('a', class_='listofdoc-level__link')
            if link:
                document = {
                    'Document Name': ' '.join(link.get_text(strip=True).split()),
                    'Date': li.get('data-copyrefdate'),
                    'Link': link['href'],
                    'Status': None,
                    'Arbitrators': ', '.join([arb[0] for arb in arbitrators]),
                    'Arbitrator Status': ', '.join([arb[1] for arb in arbitrators]),
                    'Case Name': case_name
                }
                status_dt = soup.find('dt', text='Status of the case:')
                if status_dt:
                    status_dd = status_dt.find_next('dd')
                    document['Status'] = status_dd.get_text(strip=True)
                documents.append(document)

            # Handling sub-levels
            sub_level = li.find('ul', class_='listofdoc-sublevel')
            if sub_level:
                extract_documents(sub_level, documents)

    document_list = soup.find('ul', {'class': 'listofdoc', 'id': 'listDocuments'})
    if document_list:
        extract_documents(document_list, documents)

    return documents

# Folders containing the HTML files
folders = [
    '/home/ubuntu/gpt_openai/jusmuni_html_files',
    '/home/ubuntu/gpt_openai/jusmundi_other_html'
]

all_documents = []
for folder in folders:
    for filename in os.listdir(folder):
        if filename.endswith('.html'):
            file_path = os.path.join(folder, filename)
            all_documents.extend(process_html_file(file_path))

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_documents)

# Display the DataFrame or save to a CSV file
print(df)

df.to_csv('/home/ubuntu/treaty_based_research/all.csv', index=False)