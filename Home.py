import streamlit as st
import pandas as pd

# Displaying some content in Home.py

st.set_page_config(
    page_title="TFT Carousel",
    page_icon="static/tft_icon.png",
) 

st.title("Home Page")
st.text("An introduction for anyone curious about fires!")
st.warning('This is a warning', icon="⚠️")
st.info('This is a purely informational message', icon="ℹ️")
st.error('This is an error', icon="🚨")
st.success('This is a success message!', icon="✅")

st.markdown(

    '''
    :wrench: This page is still under production! :wrench:

    '''
)