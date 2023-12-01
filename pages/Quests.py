import base64
import os

import streamlit as st
from st_clickable_images import clickable_images
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Quests",
    page_icon="😎",
    initial_sidebar_state="collapsed"
)

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
            .st-emotion-cache-1y4p8pa {
                padding: 0;
                padding-right: 10px;
                padding-left: 10px;
                padding-top: 15px;
            }
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
                margin-top: 20px;
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
            gif_html = get_img_with_href('acceptQuest.png', '/Home')
            st.markdown(gif_html, unsafe_allow_html=True)

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data()
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <hr class="rounded">
        <div class="container">
            <div class="cont">
                <p class="logo-text1">Quest summary: Summary of Quest</p>
                <p class="logo-text2">Quest description: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            </div>
            <a href="{target_url}">
            <img width="56px" heigth="56px" float="right" right="0" src="data:image/{img_format};base64,{bin_str}" />
        </a>
        </div>'''
    return html_code

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
    set_png_as_page_bg('homeBG.png') 
    quests()
    footer()

if __name__ == '__main__':
    main()