# import pandas as pd
# import streamlit as st
# from datetime import datetime
# import random

# st.set_page_config(
#     page_title="Shelter Dashboard",
#     page_icon="🏠",
# )

# from streamlit_gsheets import GSheetsConnection

# # Create a connection object.
# conn = st.connection("gsheets", type=GSheetsConnection)

# # Read the Google Sheet data with a caching mechanism to refresh every 10 seconds.
# df = conn.read(ttl="10s")

# st.write("Raw data columns from Google Sheet:", df.columns.tolist())
# st.write("Raw data sample:", df.head())

# df.columns = df.columns.str.strip()

# # Column mappings
# COLUMN_MAPPING = {
#     "DOUBLE CHECK: Choose Your Shelter": "shelter",
#     "Timestamp": "date",
#     "Water Bottle Count": "water_count",
#     "Is Water a priority?": "water_is_prio",
#     "Is Water an excess?": "water_is_excess",
#     "Clothes Count":  "cloth_count",
#     "Is Clothes a priority?": "cloth_is_prio",
#     "Is Clothes in excess?": "cloth_is_excess",
#     "Hygiene Products Count": "hyg_count",
#     "Are Hygiene Products a priority?": "hyg_is_prio",
#     "Are Hygiene Products in excess?": "hyg_is_excess",
#     "Feminine Products Count": "fem_count",
#     "Are Feminine Products a priority?": "fem_is_prio",
#     "Are Feminine Products in Excess?": "fem_is_excess",
#     "Gift Card Count": "card_count",
#     "Are Gift Cards a priority?": "card_is_prio",
#     "Are Gift Cards in excess?": "card_is_excess",
#     "Food Count": "food_count" ,
#     "Is Food a priority?": "food_is_prio",
#     "Is Food in excess?": "food_is_excess",
#     "Status": "status",
# }

# # Rename columns for consistent internal usage
# df.rename(columns=COLUMN_MAPPING, inplace=True)

# st.write("Renamed columns:", df.columns.tolist())

# if "shelter" not in df.columns:
#     st.error("The 'shelter' column is missing. Check COLUMN_MAPPING or the Google Sheet structure.")
#     st.stop()

# def status_update(shelter, response_df, status_msg=""):
#     # Filter the response dataframe for the given shelter
#     shelter_data = response_df[response_df["shelter"] == shelter]
    
#     # Convert the 'date' column to datetime format, and handle errors in conversion
#     shelter_data["date"] = pd.to_datetime(shelter_data["date"], errors="coerce")
    
#     # Find the latest entry by date
#     latest_entry = shelter_data[shelter_data["date"] == shelter_data["date"].max()]

#     # Check if we have any valid data for the shelter
#     if not latest_entry.empty:
#         status_msg = latest_entry.iloc[0]["status"]  # Example: Adjust column as needed
#         if pd.isna(status_msg):  
#             status_msg = "NaN status available for today."  # Default message for NaN
#     else:
#         status_msg = "No status available for today."
    
#     return status_msg

# def daily_priorities_and_excess(shelter, df, today_date):
#     categories = ['water', 'food', 'cloth', 'hyg', 'fem', 'card']
#     category_labels = {
#         'water': 'Water',
#         'food': 'Food',
#         'cloth': 'Clothes',
#         'hyg': 'Hygiene Products',
#         'fem': 'Feminine Products',
#         'card': 'Gift Cards'
#     }
#     for _, data_row in df.iterrows():
#         try:
#             row_date = pd.to_datetime(data_row['date'], errors='coerce').date()
#             row_shelter = data_row['shelter']
#         except ValueError:
#             continue

#         if row_date == today_date and row_shelter == shelter:
#             priority = [category_labels[cat] for cat in categories if data_row.get(f'{cat}_is_prio', '').strip().lower() == 'yes']
#             excess = [category_labels[cat] for cat in categories if data_row.get(f'{cat}_is_excess', '').strip().lower() == 'yes']
            
#             st.error(f"{', '.join(priority)}", icon="🚨")
#             st.success(f"{', '.join(excess)}", icon="✅")

# def render_shelter(shelter, city, address, email, opening_hour, closing_hour, phone_number, response_df, today_date):
#     st.subheader(shelter)
#     st.markdown(f"{city}, CA | {opening_hour} to {closing_hour}")
#     status_msg = status_update(shelter, response_df)
#     st.warning(f"{status_msg}", icon="📣")
#     tab1, tab2, tab3 = st.tabs(["At A Glance", "Reach Us", "Supplies"])

#     with tab1:
#         daily_priorities_and_excess(shelter, response_df, today_date)

#     with tab2:
#         st.markdown(f"{address}")
#         st.markdown(f"{email}")
#         st.markdown(f"{phone_number}")

#     with tab3:
#         df = pd.DataFrame(
#             {
#                 "name": ["Water", "Food", "Clothes", "Hygiene Products", "Feminine Products", "Gift Cards"],
#                 "count": [random.randint(0, 1000) for _ in range(6)],
#                 "count_history": [[random.randint(0, 5000) for _ in range(7)] for _ in range(6)],
#             }
#         )
#         st.dataframe(df)

# def main():
#     # Assume the Google Sheet has columns matching those in the updated format
#     today = datetime.today().date()
#     st.write(f"{today}")
#     st.header("Los Angeles Based Shelters", divider="gray")
    
#     # Example directory data loaded dynamically
#     directory_data = pd.DataFrame([
#         {"shelter_name": "The House LA", "city": "Los Angeles", "address": "123 Main St", 
#          "email": "houseLA@example.com", "opening_hour": "8:00 AM", "closing_hour": "8:00 PM", "phone_number": "555-1234"},
#         {"shelter_name": "Van Nuys Rec Center", "city": "Van Nuys", "address": "456 Elm St", 
#          "email": "vannuys@example.com", "opening_hour": "9:00 AM", "closing_hour": "6:00 PM", "phone_number": "555-5678"},
#     ])
    
#     cols_per_row = 2
#     for i in range(0, len(directory_data), cols_per_row):
#         cols = st.columns(cols_per_row)
#         for j, col in enumerate(cols):
#             if i + j < len(directory_data):
#                 row = directory_data.iloc[i + j]
#                 with col:
#                     render_shelter(
#                         shelter=row['shelter_name'],
#                         city=row['city'],
#                         address=row['address'],
#                         email=row['email'],
#                         opening_hour=row['opening_hour'],
#                         closing_hour=row['closing_hour'],
#                         phone_number=row['phone_number'],
#                         response_df=df,
#                         today_date=today
#                     )

# if __name__ == "__main__":
#     main()
