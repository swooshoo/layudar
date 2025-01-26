import pandas as pd
import streamlit as st
from datetime import datetime

sidebar_logo = "images/layudarlogo_large.png"
st.logo(sidebar_logo, size = "medium")

st.set_page_config(
    page_title="Community Resources",
    page_icon="images/layudarlogo.png",
)

def main():
    with st.container():
        homeicon, hometitle = st.columns([0.15,0.85])
        with homeicon:
            st.image("images/layudarlogo_large.png")
        with hometitle:
            st.header("Community Resources", divider="gray")
        st.caption("From local Google Sheets to national organizations, surf through this directory of online & local resources.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.subheader("Organizations", divider="green")
                st.link_button("LA Regional Food Bank", "https://secure.lafoodbank.org/site/Donation2?df_id=5221&mfc_pref=T&5221.donation=form1&c_src=pmax&c_src2=google-ads&gad_source=1&gclid=Cj0KCQiA7se8BhCAARIsAKnF3rw2b33NVNXsMqWUzx5E03Scala3xBgssC1bvS8jrXs945AGrD3TNbcaAtUvEALw_wcB")
                st.link_button("LA Fire Department", "https://supportlafd.kindful.com/" )
                st.link_button("LA Arts | Hammer Musuem's Fire Relief Fund", "https://hammer.ucla.edu/la-arts-community-fire-relief-fund?ct=t(COMMS_20250115_LA%20Fire%20Community%20Announcement)")
                st.link_button("SAGAFRTA Assistance Programs", "https://sagaftra.foundation/wildfire-emergency-resources/#")
        with col2:
            with st.container(border=True):
                st.subheader("GoFundMe", divider="red")
                st.link_button("Black Family Directory", "https://docs.google.com/spreadsheets/d/1pK5omSsD4KGhjEHCVgcVw-rd4FZP9haoijEx1mSAm5c/htmlview" )   
                st.link_button("Latino Family Directory", "https://docs.google.com/spreadsheets/u/3/d/1km3lEvdVY70P3875guzujp5xtoIFMr6jVZVxfpN3MeA/htmlview?fbclid=PAZXh0bgNhZW0CMTEAAabOF-0KQvmqLSxKxZJvSRMPW0eoo6-iM1J9PfUof_d_aPdR0Y1gf16OfmE_aem_RuqMdAeZ-9Om-yqNPDYeeA")                 
                st.link_button("Filipino Family Directory", "https://www.google.com/url?q=https://docs.google.com/spreadsheets/d/17hqZniTXSkz2xCXg06dLL3bV7NCnp-JROBPESwnjsgw/edit?gid%3D0%23gid%3D0&sa=D&source=editors&ust=1737705223329655&usg=AOvVaw2prLSbqfSxSchxc82JjJov")
                st.link_button("Displaced DIsabled Directory", "https://docs.google.com/spreadsheets/d/1CJeOpQWsVCo6VYXAvChXVvoYzxVJiKPn3nMTCFVMUWc/edit?gid=0#gid=0")
        
        with col3:
            with st.container(border=True):
                st.subheader("Housing", divider="blue")
                st.link_button("Dena Housing Guide", "https://docs.google.com/spreadsheets/d/1-XWt1RV3Svkejiv5I2HxZEQ5VrL_ejl40lqr0Mz2pcw/edit")
        with st.container(border=True):
            st.subheader("Add a Community Resource", divider="gray")
            st.markdown(
                '''
                Please share your known local and available resources with the Google Form below! 
                '''
            )
            st.link_button("👉 Go to Google Form ", "https://forms.gle/bpyS8CQzmnbobYUf7")
if __name__ == "__main__":  
    main()
    