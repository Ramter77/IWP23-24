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
            .container {
                display: flex;
                padding-bottom: 0px;
                margin-bottom: 0px;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:50px !important;
                color: #f9a01b !important;
                width: 50%;
            }
            .logo-img {
                width: 64px;
                height: 64px;
                margin-left: 15%;
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
            #titles=[f"Image #{str(i)}" for i in range(2)],
            titles=["Tasks", "Home", "Quests", "Diary", "Share"],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "cursor": "pointer"},
            img_style={"width": "15.5%"},
            #img_style={"margin": "5px", "width": "15.5%"},
            #img_style={"margin": "5px", "height": "200px"},
        )

        #print(clicked)
        if (clicked == 2):
            switch_page("Quests")

        clicked1 = clickable_images(
            images1,
            #titles=[f"Image #{str(i)}" for i in range(2)],
            titles=["Chat"],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "cursor": "pointer"},
            img_style={"width": "100%"},
            #img_style={"margin": "5px", "width": "100%"},
            #img_style={"margin": "5px", "height": "200px"},
        )
        #print(clicked1)
        if (clicked1 == 0):
            switch_page("Chat")
        #st.image("chatbox.png")

        #audioRecord()
        stickFooter()

def stickHeader():
    # make header sticky.
    st.markdown(
        """
            <div class='fixed-header'/>
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                    position: sticky;
                    top: 2.875rem;
                    text-color: white;
                    z-index: 999;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

def stickFooter():
    # make footer sticky.
    st.markdown(
        """
            <div class='fixed-footer'/>
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-footer) {
                    position: sticky;
                    bottom: 0%;
                    top: 28%;
                    text-color: white;
                    z-index: 999;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

def main(): 
    header()
    st.image("https://www.bwillcreative.com/wp-content/uploads/2020/05/portrait-orientation-zion-national-park.jpg")
    footer()

if __name__ == '__main__':
    main()