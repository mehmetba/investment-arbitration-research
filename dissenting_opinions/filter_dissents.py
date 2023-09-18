import pandas as pd

# File path
csv_file_path = '/home/ubuntu/treaty_based_research/all.csv'

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Filter rows where the 'Document Name' column contains the word 'dissent' (case-insensitive)
filtered_df = df[df['Document Name'].str.contains('diss', case=False)]

# Remove links containing "https://jusmundi.com"
filtered_df = filtered_df[~filtered_df['Link'].str.contains('https://jusmundi.com')]

# Finding the number of unique dissenting opinions by looking at the links
unique_dissent_links_count = filtered_df['Link'].nunique()

# Keep only unique links
filtered_df = filtered_df.drop_duplicates(subset='Link')

# Sort by the 'Case Name' column
sorted_df = filtered_df.sort_values(by='Case Name')

# Print the sorted DataFrame
print(sorted_df)

# Print the number of unique cases
unique_cases_count = sorted_df['Case Name'].nunique()
print(f'Number of unique cases: {unique_cases_count}')

# Check for duplicate links
duplicate_links = sorted_df['Link'].duplicated().sum()
print(f'Number of duplicate links: {duplicate_links}')

# Print the number of unique dissenting opinions
print(f'Number of unique dissenting opinions: {unique_dissent_links_count}')

sorted_df.to_csv('/home/ubuntu/treaty_based_research/dissent.csv', index=False)

# Select all columns except the "Link" column
df_without_link = sorted_df.drop(columns=['Link'])

# Display the DataFrame without the "Link" column
print(df_without_link)

# Optional: Save the DataFrame without the "Link" column to a new CSV file
df_without_link.to_csv('/home/ubuntu/treaty_based_research/dissent_without_link.csv', index=False)
