import base64
import os
import streamlit as st
from streamlit_extras.switch_page_button import switch_page #to switch_page without reloading

#Page config (Title, icon and collapsed sidebar)
st.set_page_config(
    page_title="Home",
    page_icon="😎",
    initial_sidebar_state="collapsed"
)

#Sidebar (saving URIprefix in session_state)
with st.sidebar:
    URIprefixValue = "thoroughly-denial-airline-device"
    if "URIpre" not in st.session_state:
        st.text_input(label="URI prefix", key="URIpre", value=URIprefixValue, placeholder=URIprefixValue, help="The URI prefix")
    else:
        st.text_input(label="URI prefix", key="URIpre", value=st.session_state.URIpre, placeholder=st.session_state.URIpre, help="The URI prefix")

    URI = f'http://{st.session_state.URIpre}.trycloudflare.com/v1/chat/completions'     #add prefix to get complete URI
    temp = st.number_input("Temperature", value=0.01, help="Default 0.01")                #set low to get deterministic results

#Header with title, currency icon and menu button
def header():
    title = "Ava"
    subtitle = "Daily motivational text"

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

#Navigation menu footer (with href instead of switch_page because using "st-clickable-images" or "st-click-detector" set a background-color which didn't work with the background image)
#On home/quests page the Home/Quests logo is bigger than the others and no margin-top
@st.cache_data()
def getFooter():
    task = os.path.splitext('task.png')[-1].replace('.', '')
    taskBinStr = getBase64OfBinFile('task.png')
    home = os.path.splitext('home.png')[-1].replace('.', '')
    homeBinStr = getBase64OfBinFile('home.png')
    quests = os.path.splitext('quests.png')[-1].replace('.', '')
    questsBinStr = getBase64OfBinFile('quests.png')
    diary = os.path.splitext('diary.png')[-1].replace('.', '')
    diaryBinStr = getBase64OfBinFile('diary.png')
    share = os.path.splitext('share.png')[-1].replace('.', '')
    shareBinStr = getBase64OfBinFile('share.png')

    chatbox = os.path.splitext('chatbox.png')[-1].replace('.', '')
    chatboxBinStr = getBase64OfBinFile('chatbox.png')

    widthHeigth = "48px"
    bigWidthHeigth = "60px"
    marginLeftRight = "10%"
    htmlCode = f"""
        <div class="cont" style="display:flex; justify-content:center; flex-wrap:wrap; cursor:pointer;">
            <a target="_self" href="{'/Home'}">
                <img width={widthHeigth} heigth={widthHeigth} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{task};base64,{taskBinStr}" />
            </a>
            <a target="_self" href="{'/Home'}">
                <img width={bigWidthHeigth} heigth={bigWidthHeigth} style="padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{home};base64,{homeBinStr}" />
            </a>
            <a target="_self" href="{'/Quests'}">
                <img width={widthHeigth} heigth={widthHeigth} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{quests};base64,{questsBinStr}" />
            </a>
            <a target="_self" href="{'/Home'}">
                <img width={widthHeigth} heigth={widthHeigth} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{diary};base64,{diaryBinStr}" />
            </a>
            <a target="_self" href="{'/Home'}">
                <img width={widthHeigth} heigth={widthHeigth} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight}; " src="data:image/{share};base64,{shareBinStr}" />
            </a>
        </div>
        <a target="_self" href="{'/Chat'}" style="display:flex; justify-content:center; flex-wrap:wrap; cursor:pointer;">
            <img width="80%" heigth="10px" style="margin-top:10px; margin-bottom:10px;" src="data:image/{chatbox};base64,{chatboxBinStr}" />
        </a>"""
    return htmlCode

def footer():
    with st.container():
        html = getFooter()
        st.markdown(html, unsafe_allow_html=True)

        stickFooter()

#Makes the header stick to the top
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

#Makes the footer stick to the bottom
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

#Returns image converted to base64
@st.cache_data()    #cache images
def getBase64OfBinFile(binFile):
    with open(binFile, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#Sets a png as the background
def setPNGasPageBG(pngFile):
    binStr = getBase64OfBinFile(pngFile)
    pageBGimg = """
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    """ % binStr
    st.markdown(pageBGimg, unsafe_allow_html=True)
    return

def main(): 
    setPNGasPageBG("homeBG.png")
    header()
    st.image("room.png", use_column_width="always")     #for now just an image
    footer()

if __name__ == '__main__':
    main()