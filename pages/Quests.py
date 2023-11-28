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
    page_title="Quests",
    page_icon="😎",
    initial_sidebar_state="collapsed"
)
#st.sidebar.success("Select a demo above.")

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
            #img_style={"margin": "5px", "height": "200px"},
        )

        #print(clicked)
        if (clicked == 1):
            switch_page("Home")

        clicked1 = clickable_images(
            images1,
            #titles=[f"Image #{str(i)}" for i in range(2)],
            titles=["Chat"],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "cursor": "pointer"},
            img_style={"width": "100%"},
            #img_style={"margin": "5px", "height": "200px"},
        )
        #print(clicked1)
        if (clicked1 == 0):
            switch_page("Chat")
        #st.image("chatbox.png")

        #audioRecord()
        stickFooter()

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

def quests():
    with st.container():
        st.markdown(
            """
            <style>
            .container {
                display: flex;
                padding-bottom: 0px;
                margin-bottom: 0px;
            }
            .cont {
                display: flex;
                padding-bottom: 0px;
                margin-bottom: 0px;
                width: 92.5%;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:50px !important;
                color: #f9a01b !important;
                width: 90%;
            }
            
            .logo-text1 {
                width: 30%;
            }
            .logo-text2 {
                width: 70%;
            }
            .logo-text3 {
                width: 90%;
            }
            .logo-img {
                width: 56px;
                height: 56px;
                float:right;
                right: 0;
            }
            .logo-img1 {
                width: 32px;
                height: 32px;
                float:right;
                right: 0;
            }
            .dashed {
                margin: 0;
                padding: 0;
                border-top: 3px dashed #fff;
            }
            hr.rounded {
                border-top: 8px solid #bbb;
                border-radius: 5px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="container">
                <p class="logo-text">Quests</p>
                <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open("reload.png", "rb").read()).decode()}">
            </div>
            """,
            unsafe_allow_html=True
        )

        questAmount = 5
        for i in range(questAmount):
            st.markdown(
                f"""
                <hr class="rounded">
                <div class="container">
                    <div class="cont">
                        <p class="logo-text1">Quest {i+1} summary: Summary of Quest number {i+1}</p>
                        <p class="logo-text2">Quest {i+1} description: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                    </div>
                    <img class="logo-img1" src="data:image/png;base64,{base64.b64encode(open("acceptQuest.png", "rb").read()).decode()}">
                </div>
                """,
                unsafe_allow_html=True
            )

def main():  
    quests()
    footer()

if __name__ == '__main__':
    main()