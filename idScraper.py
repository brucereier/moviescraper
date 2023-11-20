from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import csv
import re

def generate_monthly_dates():
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 9, 1)
    while start_date <= end_date:
        yield start_date
        if start_date.month == 12:
            start_date = datetime.date(start_date.year + 1, 1, 1)
        else:
            start_date = datetime.date(start_date.year, start_date.month + 1, 1)

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

csv_file = open("penis.csv", 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

pattern = re.compile(r'release/([^/?]+)')

for date in generate_monthly_dates():
    formatted_date = date.strftime("%Y-%m-%d")
    url = f"https://www.boxofficemojo.com/calendar/{formatted_date}/"
    driver.get(url)

    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-link-normal')))
    links = driver.find_elements(By.CLASS_NAME, 'a-link-normal')
    url_suffixes = []

    # Iterate over every second link
    for i in range(0, len(links), 2):
        href = links[i].get_attribute('href')
        match = pattern.search(href)
        if match:
            url_suffix = match.group(1)
            url_suffixes.append(url_suffix)

    csv_writer.writerow(url_suffixes)
    time.sleep(1)

driver.quit()
csv_file.close()