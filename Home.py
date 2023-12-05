import base64
import os
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
title = "Ava"
subtitle = "Daily motivational text"

def header():
    with st.container():
        st.markdown(
            """
            <style>
            div {
                background-color: transparent;
            }
            .st-emotion-cache-1y4p8pa {
                padding: 0;
                padding-right: 10px;
                padding-left: 10px;
                padding-top: 15px;
            }
            .container {
                background-color: transparent;
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
                margin-top: 10px;
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
            <div class="container" style="margin-bottom: 10px;">
                <p class="logo-text">{title}</p>
                <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open("currency.png", "rb").read()).decode()}">
                <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open("menu.png", "rb").read()).decode()}">
            </div>
            """,
            unsafe_allow_html=True
        )

        stickHeader()

@st.cache_data()
def get_footer():
    task = os.path.splitext('task.png')[-1].replace('.', '')
    task_bin_str = get_base64_of_bin_file('task.png')
    home = os.path.splitext('home.png')[-1].replace('.', '')
    home_bin_str = get_base64_of_bin_file('home.png')
    quests = os.path.splitext('quests.png')[-1].replace('.', '')
    quests_bin_str = get_base64_of_bin_file('quests.png')
    diary = os.path.splitext('diary.png')[-1].replace('.', '')
    diary_bin_str = get_base64_of_bin_file('diary.png')
    share = os.path.splitext('share.png')[-1].replace('.', '')
    share_bin_str = get_base64_of_bin_file('share.png')

    chatbox = os.path.splitext('chatbox.png')[-1].replace('.', '')
    chatbox_bin_str = get_base64_of_bin_file('chatbox.png')

    marginLeftRight = "10px"
    html_code = f'''
        <div class="container">
            <div class="cont" style="display:flex; justify-content:center; flex-wrap:wrap; cursor:pointer;">
                <a target="_self" href="{'/Home'}">
                    <img width="56px" heigth="56px" style="margin-top:4px; margin-right:{marginLeftRight}; margin-left:{marginLeftRight};" src="data:image/{task};base64,{task_bin_str}" />
                </a>
                <a target="_self" href="{'/Home'}">
                    <img width="64px" heigth="64px" style="margin-right:{marginLeftRight}; margin-left:{marginLeftRight};" src="data:image/{home};base64,{home_bin_str}" />
                </a>
                <a target="_self" href="{'/Quests'}">
                    <img width="56px" heigth="56px" style="margin-top:4px; margin-right:{marginLeftRight}; margin-left:{marginLeftRight};" src="data:image/{quests};base64,{quests_bin_str}" />
                </a>
                <a target="_self" href="{'/Home'}">
                    <img width="56px" heigth="56px" style="margin-top:4px; margin-right:{marginLeftRight}; margin-left:{marginLeftRight};" src="data:image/{diary};base64,{diary_bin_str}" />
                </a>
                <a target="_self" href="{'/Home'}">
                    <img width="56px" heigth="56px" style="margin-top:4px; margin-right:{marginLeftRight}; margin-left:{marginLeftRight};" src="data:image/{share};base64,{share_bin_str}" />
                </a>
                <a target="_self" href="{'/Chat'}">
                    <img width="100%" heigth="56px" style="margin-top:10px; margin-bottom:10px;" src="data:image/{chatbox};base64,{chatbox_bin_str}" />
                </a>
            </div>
        </div>'''
    return html_code

def footer():
    with st.container():
        html1 = get_footer()
        st.markdown(html1, unsafe_allow_html=True)

        #print(clicked1)
        #if (clicked1 == 0):
        #    switch_page("Chat")
        #st.image("chatbox.png")

        #audioRecord()
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
                    bottom: 11%;
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