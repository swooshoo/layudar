import requests
import json
import pandas as pd
import streamlit as st

def wck_webscraper():
    url = "https://wck.org/_next/data/9bT2ql8S3PlYf-75f4MDj/en-us/news/meal-locations-ca.json"
    params = {"uid": "meal-locations-ca"}

    r = requests.get(url)

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
                                        name = lines[0].strip()
                                        address = lines[1].strip()
                                        city = lines[2].strip()
                                        hours = lines[3].strip()
                                        yield {
                                            "name": name,
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
                st.dataframe(df)
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