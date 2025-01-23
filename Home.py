import streamlit as st
import pandas as pd

# Displaying some content in Home.py

st.set_page_config(
    page_title="LA Fire Shelters & Donations",
    page_icon="logo.png",
)   

st.title("LA Fire: Inventory Tracker")
with st.container(border=True):
    st.subheader("Mission Statement", divider="gray")
    st.markdown(
        '''
        Streamlining disaster relief efforts, our platform connects communities with local shelters, donation centers, and food banks in need. 
        By gathering real-time inventory updates through daily Google Form submissions, we ensure accurate and centralized information for donors and volunteers.
        Together, we make it easier to support emergency response and recovery. 
        
        ***Click the Shelters page to get started!***
        '''
    )

with st.container(border=True):
    st.subheader("Don't See Your Shelter?", divider="gray")
    st.markdown(
        '''
        Share this interest form so our team can vet and add your local shelter!
        '''
    )
    st.link_button("👉 Go to Sign-Up Form ", "https://forms.gle/1GNyKspTSEdmoW6Z7")

with st.container(border=True):
    st.subheader("FAQS", divider="gray")
    st.markdown('''
    Inspired by WatchDuty, ***THIS WEBSITE WILL NEVER BE MONETIZED***. 

    Our website will not handle any sort of online donations. You can find donation links in our Other Resource page.
    ''')
    