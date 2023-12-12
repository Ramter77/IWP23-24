import base64
import os

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Quests",
    page_icon="😎",
    initial_sidebar_state="collapsed"
)

def sidebar():
    URIprefixValue = "urls-yn-throw-painting"
    if "URIpre" not in st.session_state:
        #st.session_state.URIpre = URIprefixValue
        st.text_input(label="URI prefix", key="URIpre", value=URIprefixValue, placeholder=URIprefixValue, help="The URI prefix")    #set uri prefix from textgenUI
    else:
        st.text_input(label="URI prefix", key="URIpre", value=st.session_state.URIpre, placeholder=st.session_state.URIpre, help="The URI prefix")    #set uri prefix from textgenUI
    
    #st.write(st.session_state.URIpre)

    URI = f'http://{st.session_state.URIpre}.trycloudflare.com/v1/chat/completions'     #add prefix to get complete URI
    temp = st.number_input("Temperature", value=0.1, help="Default 0.1")   #set low to get deterministic results
    #st.session_state.URIprefix = URIprefix.value

with st.sidebar:
    sidebar()

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

        summ = ["Hat quest", "Quest summary: Summary of Quest", "Quest summary: Summary of Quest", "Quest summary: Summary of Quest", "Quest summary: Summary of Quest"]
        desc = ["Hat store quest", "Quest description: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "Quest description: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "Quest description: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "Quest description: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."]
        link = ["/QuestChat", "/Home", "/Home", "/Home", "/Home", "/Home"]
        questAmount = 5
        for i in range(questAmount):
            gif_html = get_img_with_href('acceptQuest.png', link[i], summ[i], desc[i])
            st.markdown(gif_html, unsafe_allow_html=True)

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

    widthHeigth = "48px"
    bigWidthHeigth = "60px"
    marginLeftRight = "10%"
    html_code = f'''
        <div class="cont" style="display:flex; justify-content:center; flex-wrap:wrap; cursor:pointer;">
            <a target="_self" href="{'/Home'}">
                <img width={widthHeigth} heigth={widthHeigth} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{task};base64,{task_bin_str}" />
            </a>
            <a target="_self" href="{'/Home'}">
                <img width={widthHeigth} heigth={widthHeigth} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{home};base64,{home_bin_str}" />
            </a>
            <a target="_self" href="{'/Quests'}">
                <img width={bigWidthHeigth} heigth={bigWidthHeigth} style="padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{quests};base64,{quests_bin_str}" />
            </a>
            <a target="_self" href="{'/Home'}">
                <img width={widthHeigth} heigth={widthHeigth} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{diary};base64,{diary_bin_str}" />
            </a>
            <a target="_self" href="{'/Home'}">
                <img width={widthHeigth} heigth={widthHeigth} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight}; " src="data:image/{share};base64,{share_bin_str}" />
            </a>
        </div>
        <a target="_self" href="{'/Chat'}" style="display:flex; justify-content:center; flex-wrap:wrap; cursor:pointer;">
            <img width="80%" heigth="10px" style="margin-top:10px; margin-bottom:10px;" src="data:image/{chatbox};base64,{chatbox_bin_str}" />
        </a>'''
    return html_code

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data()
def get_img_with_href(local_img_path, target_url, summ, desc):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <hr class="rounded">
        <div class="container">
            <div class="cont">
                <p class="logo-text1">{summ}</p>
                <p class="logo-text2">{desc}</p>
            </div>
            <a target="_self" href="{target_url}">
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