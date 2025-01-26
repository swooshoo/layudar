import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Contact Us",
    page_icon="images/layudarlogo.png",  
)

sidebar_logo = "images/layudarlogo_large.png"
st.logo(sidebar_logo, size = "large")

homeicon, hometitle = st.columns([0.15,0.85])
with homeicon:
    st.image("images/layudarlogo_large.png")
with hometitle:
    st.header("FAQs", divider="gray")

with st.expander("Who and Why?", icon=":material/person:"):
    st.markdown(
        '''
        University students from California who, in trying to help the fire relief effort, were unable to decide what donations to provide. 
        Seeing first-hand the sheer number of donations that overwhelmed local emergency sites, 
        we figured an inventory tracker like LAyudar could help communicate an emergency site's needs better with its community.
        
        To put it simply, people helping people.
        '''
    )
    
with st.expander("How Can We Help LAyudar?", icon=":material/person_raised_hand:"):
    st.markdown(
        '''
        As our FAQs detail, we do not handle any form of cashflow in the form of donations to us or other organizations. Running this site costs ***no money*** on our end.
        
        Please contribute via exploring our Community Resources instead!
        '''
    )
with st.expander("Where Can I Provide Feedback?", icon=":material/chat:"):
    st.markdown(
        '''
        We are open to messages and feedback. We would love to hear your thoughts!
        '''
    )
    st.link_button("👉 Go to Feedback Form ", "https://forms.gle/qpTRE9kSZYg8Gr3DA")



    