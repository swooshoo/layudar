import pandas as pd
import streamlit as st
import random

st.set_page_config(
    page_title="Shelters",
)
def load_response_data(responses_file_path):
    response_data = pd.read_csv(
        responses_file_path, skiprows=1,
        usecols=range(18),
        names =["date", "email", "shelter", "water_count", "water_is_prio", "water_is_excess", "cloth_count", "cloth_is_prio", "cloth_is_excess", 
               "hyg_count", "hyg_is_prio", "hyg_is_excess", "fem_count",
               "fem_is_prio", "fem_is_excess", "card_count", "card_is_prio", "card_is_excess"]
    )
    return response_data

def load_directory_data(directory_file_path):
    directory_data = pd.read_csv(
        directory_file_path, skiprows=1, usecols = range(7),
        names=["shelter_name", "city", "address", "email", "opening_hour", "closing_hour", "phone_number"]
    )
    return directory_data
# Display card for each unit

def load_inventory_graph(response_data):
    
    return

def render_shelter(shelter, city, address, email, opening_hour, closing_hour, phone_number):
    # Display the header with the divider color
    st.subheader(shelter.title())
    st.markdown(f"**:blue-background[{city}]**")
    st.markdown(f"**:blue-background[{opening_hour} to {closing_hour}]**")
    tab1, tab2, tab3 = st.tabs(["Needs & Extras", "Reach Us", "Full Inventory"])
    with tab1:
        col1, col2 = st.columns(2,gap="small",)
        with col1:
            
            st.write(f"**:red-background[Needs:]**")
            st.write(f"**:green-background[Can Spare:]**")                     
        with col2:
            
            st.write("Hygiene Products")
            st.write("Clothes")

    # Tab 2: Display unit ability
    with tab2:
        st.markdown(f"**Directory:**")
        st.markdown(f"{address}")
        st.markdown(f"{email}")
        st.markdown(f"{phone_number}")

    with tab3:
        df = pd.DataFrame(
            {
                "name": ["Water", "Food", "Clothes", "Hygiene Products", "Feminine Products"],
                "count": [random.randint(0, 1000) for _ in range(5)],
                "count_history": [[random.randint(0, 5000) for _ in range(7)] for _ in range(5)],
            }
        )
        
        st.dataframe(
        df,
        column_config={
            "name": "Item",
            "count": st.column_config.NumberColumn(
                "Count",
                help="Number of units of Item",
                format="%d",
            ),
            "count_history": st.column_config.BarChartColumn(
                "Count (past 7 days)", y_min=0, y_max=5000
            ),
        },
        hide_index=True,
) 
    st.subheader(" ", divider="gray")

    
def main():
    # Load data
    response_data = load_response_data("./masterShelterResponse.csv")
    directory_data = load_directory_data("./directory.csv")
    st.header("Los Angeles Based Shelters", divider = "gray")
    cols_per_row = 2 # Number of cards per row
    for i in range(0, len(directory_data), cols_per_row):
        cols = st.columns(cols_per_row)  # Create columns for each row
        for j, col in enumerate(cols):
            if i + j < len(directory_data):  # Ensure no out-of-bounds access
                row = directory_data.iloc[i + j]
                with col:
                    render_shelter(
                        shelter=row['shelter_name'],
                        city=row['city'],
                        address=row['address'],
                        email=row['email'],
                        opening_hour=row['opening_hour'],
                        closing_hour=row['closing_hour'],
                        phone_number=row['phone_number'],
                    )
    
    
        

if __name__ == "__main__":
    main()