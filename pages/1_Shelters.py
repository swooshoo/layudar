import pandas as pd
import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="Shelters",
    page_icon="logo.png",
)
def load_response_data(responses_file_path):
    response_data = pd.read_csv(
        responses_file_path, skiprows=1,
        usecols=range(22),
        names =["date", "email", "shelter", "water_count", "water_is_prio", "water_is_excess", "food_count", "food_is_prio", "food_is_excess", "cloth_count", "cloth_is_prio", "cloth_is_excess", 
               "hyg_count", "hyg_is_prio", "hyg_is_excess", "fem_count",
               "fem_is_prio", "fem_is_excess", "card_count", "card_is_prio", "card_is_excess", "status"]
    )
    return response_data

def load_directory_data(directory_file_path):
    directory_data = pd.read_csv(
        directory_file_path, skiprows=1, usecols = range(7),
        names=["shelter_name", "city", "address", "email", "opening_hour", "closing_hour", "phone_number"]
    )
    return directory_data

def status_update(shelter, response_df, status_msg=""):
    # Filter the response dataframe for the given shelter
    shelter_data = response_df[response_df['shelter'] == shelter]
    
    # Convert the 'date' column to datetime format, and handle errors in conversion
    shelter_data['date'] = pd.to_datetime(shelter_data['date'], errors='coerce')
    
    # Find the latest entry by date
    latest_entry = shelter_data[shelter_data['date'] == shelter_data['date'].max()]

    # Check if we have any valid data for the shelter
    if not latest_entry.empty:
        status_msg = latest_entry.iloc[0]['status']
    else:
        status_msg = "No status available for today."
    
    return status_msg

def daily_priorities_and_excess(shelter, df, today_date):
    categories = ['water', 'food', 'cloth', 'hyg', 'fem', 'card']
    category_labels = {
        'water': 'Water',
        'food': 'Food',
        'cloth': 'Clothes',
        'hyg': 'Hygiene Products',
        'fem': 'Feminine Products',
        'card': 'Gift Cards'
    }
    for index, data_row in df.iterrows():
        row_shelter = None
        try:
            row_date = datetime.strptime(data_row['date'], "%Y/%m/%d %H:%M:%S").date()
            row_shelter = data_row['shelter']
        except ValueError:
            try:
                row_date = datetime.strptime(data_row['date'], "%m/%d/%Y %H:%M:%S").date()
                row_shelter = data_row['shelter']
            except ValueError:
                st.error(f"Date format error in row {index}: {data_row['date']}")
                continue

        if row_date == today_date and row_shelter == shelter:
            # Convert categories using the dictionary
            priority = [category_labels[cat] for cat in categories if data_row[f'{cat}_is_prio'].strip().lower() == 'yes']
            excess = [category_labels[cat] for cat in categories if data_row[f'{cat}_is_excess'].strip().lower() == 'yes']
            
            #st.markdown(f"**:red-background[{', '.join(priority)}]**")
            #st.markdown(f"**:green-background[{', '.join(excess)}]**")
            st.success(f"{', '.join(excess)}", icon="✅")
            st.error(f"{', '.join(priority)}", icon="🚨")
            
def generate_weekly_df(shelter, response_df, today_date):
    # Define the category labels for clarity
    category_labels = {
        'water_count': 'Water',
        'food_count': 'Food',
        'cloth_count': 'Clothes',
        'hyg_count': 'Hygiene Products',
        'fem_count': 'Feminine Products',
        'card_count': 'Gift Cards'
    }
    
    # Filter data for the specified shelter and the last 7 days
    last_7_days_data = response_df[
        (response_df['shelter'] == shelter) &
        (pd.to_datetime(response_df['date'], errors='coerce').dt.date >= today_date - pd.Timedelta(days=6))
    ]

    # Prepare the counts and history for the dataframe
    weekly_counts = {}
    count_history = {label: [] for label in category_labels.values()}

    for index, row in last_7_days_data.iterrows():
        for col, label in category_labels.items():
            count_history[label].append(row[col])  # Collect count data

    # Generate the most recent count as the latest entry for each item
    for col, label in category_labels.items():
        most_recent_count = last_7_days_data.iloc[-1][col] if not last_7_days_data.empty else 0
        weekly_counts[label] = most_recent_count

    # Convert data into a DataFrame for Streamlit
    weekly_df = pd.DataFrame({
        "name": list(category_labels.values()),
        "count": [weekly_counts[label] for label in category_labels.values()],
        "count_history": [count_history[label] for label in category_labels.values()]
    })
    return weekly_df

def render_shelter(shelter, city, address, email, opening_hour, closing_hour, phone_number, response_df, today_date):
    # Display the header with the divider color
    with st.container(border=True):
        st.subheader(shelter)
        #st.markdown(f"**:blue-background[{city}, CA] | {opening_hour} to {closing_hour}**")
        st.markdown(f"{city}, CA | {opening_hour} to {closing_hour}")
        
        # Initialize an empty string for status message
        status_msg = ""
            # Call the helper function to get the latest status
        status_msg = status_update(shelter, response_df, status_msg)
            # Display the status update
        #t.markdown(f"**{shelter} says:**")
        st.warning(f"{status_msg}",icon="📣")   

        tab1, tab2, tab3 = st.tabs(["At A Glance", "Reach Us", "Supplies"])
        
        with tab1:
            daily_priorities_and_excess(shelter, response_df,today_date)
        # Tab 2: Display unit ability
        with tab2:
            st.markdown(f"**Directory:**")
            st.markdown(f"{address}")
            st.markdown(f"{email}")
            st.markdown(f"{phone_number}")

        with tab3:
            weekly_df = generate_weekly_df(shelter, response_df, today_date)
            
            st.dataframe(
                weekly_df,
                column_config={
                    "name": st.column_config.TextColumn(
                        "Item",
                        disabled=True,
                    ),
                    "count": st.column_config.NumberColumn(
                        "Count",
                        help="Number of units of Item",
                        disabled=True,
                        format="%d",
                    ),
                    "count_history": st.column_config.BarChartColumn(
                        "Count (past 7 days)",
                        y_min=0, 
                        y_max=400,
                    ),
                },
                hide_index=True,
                on_select="ignore",
            ) 

def main():
    # Load data
    response_data = load_response_data("./masterShelterResponse.csv")
    directory_data = load_directory_data("./directory.csv")
    today = datetime.today().date()
    st.write(f"{today}")
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
                        response_df=response_data,
                        today_date=today
                    )

if __name__ == "__main__":
    main()