import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Home - LAyudar",
    page_icon="images/layudarlogo.png",  
)

sidebar_logo = "images/layudarlogo_big.png"
st.logo(sidebar_logo, size = "large")

homeicon, hometitle = st.columns([0.25,0.75])

with homeicon:
    st.image("images/layudarlogo_big.png")
with hometitle:
    st.title("LAyudar")
    st.subheader("A Centralized Resource for LA Fire Relief")

with st.container(border=True):
    st.subheader("Mission Statement", divider="gray")
    st.markdown(
        '''
        We saw a need to centralize all of the legitimate and local resources out there for emergency relief, volunteer opportunities, and etc.
        
        Streamlining disaster relief efforts, **LAyudar** connects communities with local shelters, donation centers, and food banks in need. 
        By gathering real-time inventory updates through daily Google Form submissions, we ensure accurate and centralized information for donors and volunteers.
        Together, we make it easier to support emergency response and recovery. 
        '''
    )

with st.container(border=True):
    st.subheader("Don't See A Site?", divider="gray")
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
    
    We are open to feedback and scaling. We would love to hear your thoughts!
    ''')
    st.link_button("👉 Go to Survey Form ", "https://forms.gle/rfRjcLDgXYAy8Ge49")
    