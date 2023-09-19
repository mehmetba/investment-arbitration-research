#buna gerek kalmadı jsmndi nin sitemap buldum ama google serp analizi icin guzel
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



# Set up Firefox WebDriver
options = Options()
options.headless = True  # Run Firefox in headless mode (without GUI)
driver = webdriver.Firefox(options=options)

# Load Google search page
url = 'https://www.google.com/'
driver.get(url)

# Search for your keyword (modify 'search_term' as needed)
search_box = driver.find_element(By.NAME, 'q')
search_term = ' site:jusmundi.com'  # Modify this with your keyword

# Define your search query and target website
search_query = "NJSC Naftogaz of Ukraine, PJSC State Joint Stock Company Chornomornaftogaz, PJSC Ukrgasvydobuvannya and others v. The Russian Federation, PCA Case No. 2017-16, Dissenting Opinion of Professor Dr. Maja Stanivuković."
target_site = "site:jusmundi.com"  # Replace example.com with the website you want to search within

search_term=f"{search_query}+{target_site}"

search_box.send_keys(search_term)
search_box.send_keys(Keys.RETURN)

num = 1

# Scrape multiple pages
for page in range(1, 6):  # Scrape the first 5 pages of results
    # Wait for the search results page to load
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.g'))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    # Parse the search results
    search_results = driver.find_elements(By.CSS_SELECTOR, '.g')
    for result in search_results:
        link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        title = result.find_element(By.CSS_SELECTOR, 'h3').text
        print(num)
        print(title)
        print(link)
        num = num + 1

    # Click on the next page
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, '#pnnext')
        next_button.click()
    except:
        break

# Close the Firefox WebDriver
driver.quit()
