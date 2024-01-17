import streamlit as st
import base64
import os
from st_click_detector import click_detector
#from streamlit_extras.switch_page_button import switch_page #to switch_page without reloading

#Page config (Title, icon and collapsed sidebar)
st.set_page_config(
    page_title="Home",
    page_icon="😎",
    initial_sidebar_state="collapsed"
)

#Sidebar (saving URIprefix in session_state)
with st.sidebar:
    URIprefixValue = "urls-yn-throw-painting"
    if "URIpre" not in st.session_state:
        st.text_input(label="URI prefix", key="URIpre", value=URIprefixValue, placeholder=URIprefixValue, help="The URI prefix")
    else:
        st.text_input(label="URI prefix", key="URIpre", value=st.session_state.URIpre, placeholder=st.session_state.URIpre, help="The URI prefix")

    URI = f'http://{st.session_state.URIpre}.trycloudflare.com/v1/chat/completions'     #add prefix to get complete URI
    temp = st.number_input("Temperature", value=0.01, help="Default 0.01")                #set low to get deterministic result


startingMoney = 100
#Init session state
if 'text' not in st.session_state:
    st.session_state['text'] = 'Let’s go clothes shopping!'
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'oldCounter' not in st.session_state:
    st.session_state['oldCounter'] = 0
if 'currentChoice' not in st.session_state:
    st.session_state['currentChoice'] = ""
if 'money' not in st.session_state:
    st.session_state['money'] = startingMoney         #Start with 100 Euros


#EDIT THESE
#Text array
moneyThreshold = 20
optionsDict = {"Blue Hat": 10, "Red Hat": 30, "Brown Coat": 40, "Black Coat": 30, "White Shoes": 40, "Orange Shoes": 30}
print("Current choice: " + str(st.session_state['currentChoice']))
texts = ["Let’s go clothes shopping!", "You have €100. You need to have at least €20 for groceries after your clothes shopping", "First, let’s buy a new hat!", "There are 2 hats. The blue hat costs €10. The red hat costs €30.", "Which hat do you want to buy?", "Great! You bought the " + str(st.session_state['currentChoice']) + " ! You now have €" + str(st.session_state['money']) + " .", "Let’s continue with the clothes shopping.", "Let’s buy a new coat!", "There are 2 coats. The brown coat costs €40. The black coat costs €30.", "Which coat do you want to buy?", "Great! You bought the ____ coat! You now have €____.", "Let’s continue with the clothes shopping.", "Let’s buy new shoes!", "There are 2 pairs of shoes. The white shoes cost €40. The orange shoes cost €30.", "Which pair of shoes do you want to buy?", "Good job! You still have €20 after your clothes shopping!", "Do you want to try again?"]
print("Texts length")
print(len(texts))

useContainerWidth = True

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

st.header("Quest")
st.markdown("""<h3 style="padding:0;">Clothes shopping</h3>""", unsafe_allow_html=True)
#st.subheader("Clothes shopping")
setPNGasPageBG("homeBG.png")
arrowBack = ":arrow_backward:"          #👈
arrowForward = ":arrow_forward:"        #👉
    
#Changes the text depending on the choice
def changeText(choice):
    #Debug print text and counter
    print(st.session_state['text'] + " and counter: " + str(st.session_state['counter']))

    #Choices
    if choice == "Forward":
        st.session_state['counter'] += 1
    elif choice == "Back":
        if (st.session_state['counter'] > 0):
            st.session_state['counter'] -= 1

    if st.session_state['counter'] == 5:
        st.session_state['text'] = "Great! You bought the " + str(st.session_state['currentChoice']) + " ! You now have €" + str(st.session_state['money']) + " ."
    elif st.session_state['counter'] == 10:
        st.session_state['text'] = "Great! You bought the " + str(st.session_state['currentChoice']) + " ! You now have €" + str(st.session_state['money']) + " ."
    elif st.session_state['counter'] == 15:
        #Check if the remaining money is higher or equal to the threshold
        if st.session_state['money'] >= moneyThreshold:
            st.session_state['text'] = "Great! You bought the " + str(st.session_state['currentChoice']) + " ! You now have €" + str(st.session_state['money']) + " ."
        else:
            st.session_state['text'] = "You bought the " + str(st.session_state['currentChoice']) + " ! Unfortunately, you now have only €" + str(st.session_state['money']) + " ."
    else:
        st.session_state['text'] = texts[st.session_state['counter']]


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

    width = "48px"
    bigWidth = "60px"
    marginLeftRight = "10%"
    htmlCode = f"""
        <div class="cont" style="display:flex; justify-content:center; flex-wrap:wrap; cursor:pointer;">
            <a target="_self" href="{'/'}">
                <img width={width} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{task};base64,{taskBinStr}" />
            </a>
            <a target="_self" href="{'/'}">
                <img width={bigWidth} style="padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{home};base64,{homeBinStr}" />
            </a>
            <a target="_self" href="{'/'}">
                <img width={width} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{quests};base64,{questsBinStr}" />
            </a>
            <a target="_self" href="{'/'}">
                <img width={width} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight};" src="data:image/{diary};base64,{diaryBinStr}" />
            </a>
            <a target="_self" href="{'/'}">
                <img width={width} style="margin-top:4px; padding-right:{marginLeftRight}; padding-left:{marginLeftRight}; " src="data:image/{share};base64,{shareBinStr}" />
            </a>
        </div>
        <a target="_self" href="{'/'}" style="display:flex; justify-content:center; flex-wrap:wrap; cursor:pointer;">
            <img width="256px" height="25px" style="margin-top:10px; margin-bottom:10px;" src="data:image/{chatbox};base64,{chatboxBinStr}" />
        </a>"""
    return htmlCode

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

def footer():
    with st.container():
        html = getFooter()
        st.markdown(html, unsafe_allow_html=True)

        stickFooter()

def changeText2(key, value):
    #print(list(optionsDict.keys())[0])
    print(key)
    print(value)
    #print(list(optionsDict.keys()))
    print("--------------------------")
    

    st.session_state['currentChoice'] = key
    st.session_state['money'] -= int(value)

    #Always go next
    changeText('Forward')

def numButtons(num1, num2):
    key1 = list(optionsDict.keys())[num1]
    key2 = list(optionsDict.keys())[num2]
    value1 = list(optionsDict.values())[num1]
    value2 = list(optionsDict.values())[num2]

    colT1,colT2 = st.columns(2)
    with colT1:
        st.button(str(key1), use_container_width=useContainerWidth, on_click=changeText2, args=[key1, value1], type="primary")
            
    with colT2:
        st.button(str(key2), use_container_width=useContainerWidth, on_click=changeText2, args=[key2, value2], type="primary")

def navButtons(back, forward):
    useImages = False
    if useImages:
        back = os.path.splitext('denyQuest.png')[-1].replace('.', '')
        backBinStr = getBase64OfBinFile('denyQuest.png')
        forward = os.path.splitext('acceptQuest.png')[-1].replace('.', '')
        forwardBinStr = getBase64OfBinFile('acceptQuest.png')

        content = f"""
            <a href='#' id='Image 1'><img width='50px' style="float:left;" src="data:image/{back};base64,{backBinStr}"></a>
            <a href='#' id='Image 2'><img width='50px' style="float:right;" src="data:image/{forward};base64,{forwardBinStr}"></a>
            """
        clicked = click_detector(content)

        if clicked == "Image 1":
            changeText("Back")
        elif clicked == "Image 2":
            changeText("Forward")
        
    else:
        #Use columns
        if back and forward:
            colT1,colT2 = st.columns(2)
            with colT1:
                st.image("denyQuest.png", width=64)
                st.button(arrowBack, use_container_width=useContainerWidth, on_click=changeText, args=['Back'], type="secondary")
            with colT2:
                st.image("acceptQuest.png", width=64)
                st.button(arrowForward, use_container_width=useContainerWidth, on_click=changeText, args=['Forward'], type="secondary")
        
        #Dont use columns
        elif back:
            st.button(arrowBack, use_container_width=True, on_click=changeText, args=['Back'], type="secondary")
        elif forward:
            st.button(arrowForward, use_container_width=True, on_click=changeText, args=['Forward'], type="secondary")

#UI
with st.container(border=True):
    cat = os.path.splitext('cat.png')[-1].replace('.', '')
    catBinStr = getBase64OfBinFile('cat.png')
    gem = os.path.splitext('currency.png')[-1].replace('.', '')
    gemBinStr = getBase64OfBinFile('currency.png')

    width1 = "64px"
    width2 = "40px"
    html = f"""
        <img width={width1} style="margin-top:17.5px;" src="data:image/{cat};base64,{catBinStr}" />

        <div style="float:right; display:flex; flex-wrap:wrap;">
                <img width={width2} height={width2} style="margin-top:0px;" src="data:image/{gem};base64,{gemBinStr}" /> 
                <h1 style="padding:0; float:right;">{"€"+str(st.session_state['money'])}</h1>
        </div>"""

    st.markdown(html, unsafe_allow_html=True)

    #<h1 style="padding-left:90px; float:right;">{"💰 €"+str(st.session_state['money'])}</h1>
    #<div class="cont" style="height:30px; display:flex; flex-wrap:wrap; margin-bottom:0px; padding-bottom:0px;">

    #colT1,colT2 = st.columns([0.1,0.9])
    #with colT1:
    #    st.image("cat.png", width=64)
    #    print("cat image")
    #with colT2:
    #    #st.image("gems.png", width=64)
    #    st.subheader("💰 €"+str(st.session_state['money']))

    st.text_area("Text", height=10, value=st.session_state['text'], label_visibility="collapsed")       #disabled=True turns off interactivity but also grays it out
    
    #if (st.session_state['counter'] == -1):
    #    st.button("Back", use_container_width=True, on_click=changeText, args=['Back'], type="primary")
    if (st.session_state['counter'] == 0):
        navButtons(False, True)

    elif (st.session_state['counter'] == 4):
        navButtons(True, False)
        numButtons(0, 1)
    elif (st.session_state['counter'] == 5):
        navButtons(False, True)

    elif (st.session_state['counter'] == 9):
        navButtons(True, False)
        numButtons(2, 3)
    elif (st.session_state['counter'] == 10):
        navButtons(False, True)

    elif (st.session_state['counter'] == 14):
        navButtons(True, False)
        numButtons(4, 5)
    elif (st.session_state['counter'] == 15):
        #navButtons(False, True)
        if st.session_state['money'] >= moneyThreshold:
            print("You Won")
        else:
            navButtons(False, True)
        #print("END")

    elif (st.session_state['counter'] == 16):
        if st.button("Try again", use_container_width=True, type="primary"):
                st.session_state['text'] = 'Let’s go clothes shopping!'
                st.session_state['counter'] = 0
                st.session_state['oldCounter'] = 0
                st.session_state['currentChoice'] = ""
                st.session_state['money'] = 100
                st.rerun()
          
    #elif (st.session_state['counter'] > len(texts)):
    #    print("--------------------END-------------------")
    else:
        navButtons(True, True)


footer()







        ####
    #colT1,colT2 = st.columns([0.25,0.75])
    #with colT2:
        #st.image("hats.png", width=256)

    #    colTT1,colTT2 = st.columns([0.4,0.6])
    #    with colTT1:
    #        st.image("cat.png", width=64)
    #        print("cat image")
    #    with colTT2:
    #        #st.image("gems.png", width=64)
    #        st.write("💰 €"+str(st.session_state['money']))
