from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import re
# Initialize the WebDriver
driver = webdriver.Firefox()
header = ["Budget", "MPAARating", "Genre", "Distributor", "Runtime"]

# Append day-specific headers for 30 days
for day in range(1, 31):
    header.extend([
        f"Day{day}Date", 
        f"Day{day}DOW", 
        f"Day{day}BoxOffice", 
        f"Day{day}Theaters", 
        f"Day{day}ToDate"
    ])

# Create and open the file, then write the header


def get_row_data(row_element):
    # Find all the <td> elements in the row
    columns = row_element.find_elements(By.TAG_NAME, "td")
    
    # Extract the text from the required columns
    date = columns[0].text.split('\n')[0] # First column for date
    if '-' in date:
        return None
    day_of_week = columns[1].text  # Second column for day of week
    daily_box_office = columns[3].text  # Fourth column for daily box office
    box_integer = int(re.sub(r'[\$,]', '', daily_box_office))
    theaters = columns[6].text.replace(',', '')
    box_office_to_date = columns[8].text  # Ninth column for box office to date
    boxtd_int = int(re.sub(r'[\$,]', '', box_office_to_date))
    
    # Return the data as a list
    return [date, day_of_week, box_integer, theaters, boxtd_int]
# Function to open and process each URL
def process_url(release_id):
    url = f"https://www.boxofficemojo.com/release/{release_id}/?ref_=bo_rs_table_23"
    driver.get(url)
    try:
        domestic_daily_link = driver.find_element(By.XPATH, "//a[@class='a-size-base a-link-normal mojo-navigation-tab mojo-navigation-tab-active' and contains(text(), 'Domestic Daily')]")
        try:
            bud_label = driver.find_element(By.XPATH, "//span[contains(text(), 'Budget')]")
        
        # Find the next sibling span which contains the genre value
            bud_val = bud_label.find_element(By.XPATH, "./following-sibling::span")
            dollar_amount = bud_val.text
            # Remove dollar sign and commas, then convert to integer
            amount_integer = int(re.sub(r'[\$,]', '', dollar_amount))
        except NoSuchElementException:
            print(f"Element not found for URL: {url}")
            amount_integer = None

        try:
            mpaa_label = driver.find_element(By.XPATH, "//span[contains(text(), 'MPAA')]")
        
        # Find the next sibling span which contains the genre value
            mpaa_val = mpaa_label.find_element(By.XPATH, "./following-sibling::span")
            rating = mpaa_val.text
        except:
            rating = None

        runtime_xpath = "/html/body/div[1]/main/div/div[3]/div[4]/div[6]/span[2]"
        try:
            runtime_label = driver.find_element(By.XPATH, "//span[contains(text(), 'Running Time')]")
        
        # Find the next sibling span which contains the genre value
            runtime_val = runtime_label.find_element(By.XPATH, "./following-sibling::span")
            runtime = runtime_val.text
        except:
            runtime = None

        try:
            genres_label = driver.find_element(By.XPATH, "//span[contains(text(), 'Genres')]")
        
        # Find the next sibling span which contains the genre value
            genres_value = genres_label.find_element(By.XPATH, "./following-sibling::span")
            genre = genres_value.text
        except:
            genre = None

        try:
            dist_label = driver.find_element(By.XPATH, "//span[contains(text(), 'Distributor')]")
        
        # Find the next sibling span which contains the genre value
            dist_value = dist_label.find_element(By.XPATH, "./following-sibling::span")
            distributor_raw = driver.execute_script("return arguments[0].textContent;", dist_value)
            distributor = distributor_raw.split("See")[0].strip()

        except:
            distributor = None
        
        cur = [amount_integer, rating, genre, distributor, runtime]
        #print(cur)

        try:
        # Find the tbody element
            tbody = driver.find_element(By.TAG_NAME, "tbody")
            
            # Get all the rows in the tbody, skipping the first row
            rows = tbody.find_elements(By.TAG_NAME, "tr")[1:31]  # Skip the first row and limit to first 30 rows

            # Check if there are at least 30 rows of data
            if len(rows) < 30:
                print("Less than 30 rows of data, skipping...")
            else:
                for row in rows:
                    try:
                        row_data = get_row_data(row)  # Extract the data from the row
                        cur.extend(row_data)  # Append the data to the all_rows_data list
                    except IndexError:
                        # If there are not enough columns, skip this row
                        print("Row doesn't have all the required columns, skipping...")
                        continue
                writer.writerow(cur)

        except NoSuchElementException:
            print("No tbody element found on this page.")
    except:
        print("Domestic Daily not found")
        return

# Open and read the CSV file
with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    with open('links2.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            for release_id in row:
                process_url(release_id)
                time.sleep(1)  # Throttle requests

# Close the WebDriver
driver.quit()
