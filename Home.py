import base64
import json
from pathlib import Path
import streamlit as st
from st_click_detector import click_detector
from st_clickable_images import clickable_images
import requests
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import streamlit_chat

st.set_page_config(
    page_title="Home",
    page_icon="😎",
    initial_sidebar_state="collapsed"
)
#st.sidebar.success("Select a demo above.")

#UI
title = "Petname"
subtitle = "Daily motivational text"

def header():
    with st.container():
        st.markdown(
            """
            <style>
            .st-emotion-cache-1y4p8pa {
                padding: 0;
                padding-right: 10px;
                padding-left: 10px;
                padding-top: 15px;
            }
            .container {
                height: 50px;
                background: none;
                display: flex;
                padding-bottom: 0px;
                margin-bottom: 0px;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:50px !important;
                color: #f9a01b !important;
                width: 100%;
                margin-bottom: 0%;
            }
            .logo-img {
                width: 40px;
                height: 40px;
                margin-top: 20px;
                margin-left: 2%;
                float:right;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="container">
                <p class="logo-text">{title}</p>
                <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open("currency.png", "rb").read()).decode()}">
                <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open("menu.png", "rb").read()).decode()}">
            </div>
            """,
            unsafe_allow_html=True
        )

        stickHeader()

def footer():
    images = []
    for file in ["task.png", "home.png", "quests.png", "diary.png", "share.png"]:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")

    images1 = []
    with open("chatbox.png", "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images1.append(f"data:image/jpeg;base64,{encoded}")

    with st.container():
        clicked = clickable_images(
            images,
            titles=["Tasks", "Home", "Quests", "Diary", "Share"],
            div_style={"display": "flex", "background-color": "transparent", "justify-content": "center", "flex-wrap": "wrap", "cursor": "pointer"},
            img_style={"width": "15.5%"},
        )

        if (clicked == 2):
            switch_page("Quests")

        clicked1 = clickable_images(
            images1,
            titles=["Chat"],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "cursor": "pointer"},
            img_style={"width": "100%"},
        )

        if (clicked1 == 0):
            switch_page("Chat")

        stickFooter()

def stickHeader():
    st.markdown(
        """
            <div class='fixed-header'/>
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                    position: sticky;
                    top: 0rem;
                    z-index: 999;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

def stickFooter():
    st.markdown(
        """
            <div class='fixed-footer'/>
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-footer) {
                    position: sticky;
                    bottom: 0%;
                    top: 28%;
                    z-index: 999;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def main(): 
    header()
    st.image("room.png", use_column_width="always")
    footer()

if __name__ == '__main__':
    set_png_as_page_bg('homeBG.png')
    main()