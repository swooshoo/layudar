import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Shelters",
    page_icon="logo.png",
)

# Initialize Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def load_response_data():
    response_data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1wrgKccuaPqvIOTtTcmyUSYmuBwRgiuC8BajDx_WItcM/edit?gid=1517021569#gid=1517021569", ttl="10s")
    response_data.columns = [
        "date", "email", "shelter", "water_count", "water_is_prio", "water_is_excess",
        "food_count", "food_is_prio", "food_is_excess", "cloth_count", "cloth_is_prio", "cloth_is_excess",
        "hyg_count", "hyg_is_prio", "hyg_is_excess", "fem_count", "fem_is_prio", "fem_is_excess",
        "card_count", "card_is_prio", "card_is_excess", "status"
    ]
    return response_data

def load_directory_data():
    directory_data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1wrgKccuaPqvIOTtTcmyUSYmuBwRgiuC8BajDx_WItcM/edit?gid=1785591436#gid=1785591436", ttl="10s")
    directory_data.columns = [
        "shelter_name", "city", "address", "email", "opening_hour", "closing_hour", "phone_number"
    ]
    return directory_data

def status_update(shelter, response_df):
    shelter_data = response_df[response_df['shelter'] == shelter]
    shelter_data['date'] = pd.to_datetime(shelter_data['date'], errors='coerce')
    latest_entry = shelter_data.loc[shelter_data['date'].idxmax()]
    return latest_entry['status'] if not shelter_data.empty else "No status available for today."

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
    shelter_data = df[(df['shelter'] == shelter) & (pd.to_datetime(df['date'], errors='coerce').dt.date == today_date)]
    if not shelter_data.empty:
        row = shelter_data.iloc[0]
        priority = [category_labels[cat] for cat in categories if row[f'{cat}_is_prio'].strip().lower() == 'yes']
        excess = [category_labels[cat] for cat in categories if row[f'{cat}_is_excess'].strip().lower() == 'yes']
        st.success(f"Excess: {', '.join(excess)}", icon="✅")
        st.error(f"Priority: {', '.join(priority)}", icon="🚨")

def render_shelter(shelter, city, address, email, opening_hour, closing_hour, phone_number, response_df, today_date):
    with st.container(border=True):
        st.subheader(shelter)
        st.markdown(f"{city}, CA | {opening_hour} to {closing_hour}")
        status_msg = status_update(shelter, response_df)
        st.warning(status_msg, icon="📣")

        tab1, tab2 = st.tabs(["At A Glance", "Reach Us"])
        with tab1:
            daily_priorities_and_excess(shelter, response_df, today_date)
        with tab2:
            st.markdown(f"**Address:** {address}")
            st.markdown(f"**Email:** {email}")
            st.markdown(f"**Phone:** {phone_number}")

def main():
    response_data = load_response_data()
    directory_data = load_directory_data()
    today = datetime.today().date()

    st.header("Los Angeles Based Shelters", divider="gray")
    cols_per_row = 2

    for i in range(0, len(directory_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(directory_data):
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
