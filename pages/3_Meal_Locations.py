import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="Meal Locations",
    page_icon="images/layudarlogo.png",  
)

def wck_webscraper():
    # Step 1: Set up the Chrome WebDriver with Selenium
    options = Options()
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")  # Updated headless mode
    options.add_argument("--no-sandbox")  # Avoid sandbox issues
    options.add_argument("--disable-dev-shm-usage")  # Fix shared memory issue
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    
    chrome_driver_path = ChromeDriverManager().install()
    service = ChromeService(chrome_driver_path)
    
    driver = webdriver.Chrome(service=service, options=options)

    # Step 2: Navigate to the webpage
    url = 'https://wck.org/news/meal-locations-ca'
    driver.get(url)

    # Step 3: Wait for content to load
    time.sleep(5)

    # Step 4: Find the content div by its class name
    content_div = driver.find_element(By.CLASS_NAME, 'styles__Content-sc-16eeiua-2')

    # Step 5: Extract the HTML content of the div
    content_html = content_div.get_attribute('outerHTML')

    # Step 6: Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content_html, 'html.parser')

    # # Step 7: Find all <p> elements inside the div
    paragraphs = soup.find_all('p')

    # # Step 8: Print the contents of each <p> element
    # for paragraph in paragraphs:
    #     print(paragraph.get_text())

    # # Step 9: Close the browser
    # driver.quit()

    # Step 7: Create a list to hold the extracted data
    data = []

    # Step 8: Iterate over each <p> tag and extract the required data
    for paragraph in paragraphs:
        # Extract the location name (text inside the <strong> tag)
        location_name = paragraph.find('strong').get_text(strip=True) if paragraph.find('strong') else ''
        
        # Extract all the text parts separated by <br> tags
        text_parts = [text.strip() for text in paragraph.stripped_strings]
        
        # Make sure there are at least 4 parts (location name, address, city, operating hours)
        if len(text_parts) >= 4:
            address = text_parts[1]  # Address is the second part
            city = text_parts[2]     # City is the third part
            operating_hours = text_parts[3]  # Operating hours is the fourth part
            # Append the data to the list
            data.append([location_name, address, city, operating_hours])

    # Step 9: Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=['Location Name', 'Address', 'City', 'Operating Hours'])

    # Step 10: Display the DataFrame
    st.dataframe(df)

    # Optional: Save the DataFrame to a CSV file
    # df.to_csv('locations.csv', index=False)

def main():
    homeicon, hometitle = st.columns([0.15,0.85])
    with homeicon:
        st.image("images/layudarlogo_large.png")
    with hometitle:
        st.header("Meal Distribution Sites")
        st.subheader("by World Central Kitchen", divider="gray")
    st.caption("Daily Updated Meal Locations from the WCK website.")
    st.info("This page is still under development!")
    
    wck_webscraper()

if __name__ == "__main__":
    main()
