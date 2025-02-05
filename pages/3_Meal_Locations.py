import requests
import json
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

def wck_webscraper():
    r = requests.get("https://wck.org/news/meal-locations-ca")
    soup = BeautifulSoup(r.text, "html.parser")
    script_tags = soup.find_all("script", defer="")

    build_id = None  # Initialize build_id to None

    for tag in script_tags:
        if tag.has_attr('src') and "_buildManifest.js" in tag['src']: # Check if 'src' exists
            build_id = tag['src'].split("/")[-2]
            break  # Exit the loop once you find it

    if build_id is None:
        print("Error: Could not find build ID.")  # Handle the case where it's not found
        return  # Or raise an exception, or return a default value, as needed

    r = requests.get(
        f"https://wck.org/_next/data/{build_id}/en-us/news/meal-locations-ca.json?uid=meal-locations-ca"
    )

    if r.status_code == 200:
        try:
            data = r.json()
            locations = []

            try:
                # ***NEW, HIGHLY FLEXIBLE JSON PARSING***
                def extract_locations(data):
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if key == 'text' and isinstance(value, str) and '\n' in value: #check for newline
                                lines = value.split('\n')
                                if len(lines) >= 4:
                                    try:
                                        site = lines[0].strip()
                                        address = lines[1].strip()
                                        city = lines[2].strip()
                                        hours = lines[3].strip()
                                        yield {
                                            "site": site,
                                            "address": address,
                                            "city": city,
                                            "hours": hours
                                        }
                                    except IndexError:
                                        st.warning(f"Skipping malformed location data: {value}")
                                        print(f"Malformed location data: {value}")
                            else:
                                yield from extract_locations(value)  # Recursively search

                    elif isinstance(data, list):
                        for item in data:
                            yield from extract_locations(item)  # Recursively search

                locations = list(extract_locations(data)) # Convert generator to list
                

            except Exception as e: # Catch a broader range of exceptions
                st.error(f"Error parsing JSON: {e}. The website structure may have changed.")
                print(f"Error parsing JSON: {e}. JSON Data: {data}")

            if locations:
                df = pd.DataFrame(locations)
                #st.dataframe(df)
            else:
                st.write("No meal location data found.")

        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON response: {e}")
            print(f"Invalid JSON response: {e}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching URL: {e}")
            print(f"Error fetching URL: {e}")

    else:
        st.error(f"Request failed with status code: {r.status_code}")
        print(f"Request failed with status code: {r.status_code}")
        
    return df

def render_meal_dir(site, address, city, hours):
    with st.container(border=True):
        st.subheader(site, divider="orange")
        col1, col2, col3 = st.columns(3) #unused column for alignment purposes
        with col1:
            st.write(f"{city}")
        with col3:
            st.write(f"{hours}")
            
        st.code(f"{address}",wrap_lines=True)

def main():
    homeicon, hometitle = st.columns([0.15,0.85])
    with homeicon:
        st.image("images/layudarlogo_large.png")
    with hometitle:
        st.header("WCK Meal Distribution Directory", divider="gray")
        
    tip1, tip2 = st.columns([.65,.35])
    with tip1:
        st.markdown(":material/public: By the [World Central Kitchen](https://wck.org/news/meal-locations-ca)")
    with tip2:
        st.caption("Copy an address with the :material/content_copy: button!")
    
    meal_df = wck_webscraper()
    
    cols_per_row = 2 # Number of cards per row
    for i in range(0, len(meal_df), cols_per_row):
        cols = st.columns(cols_per_row)  # Create columns for each row
        for j, col in enumerate(cols):
            if i + j < len(meal_df):  # Ensure no out-of-bounds access
                row = meal_df.iloc[i + j]
                with col:
                    render_meal_dir(
                        site=row['site'],
                        address=row['address'],
                        city=row['city'],
                        hours=row['hours'],
                    )

if __name__ == "__main__":
    main()