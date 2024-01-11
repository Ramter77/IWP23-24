import streamlit as st
#from st_click_detector import click_detector
from streamlit_extras.switch_page_button import switch_page #to switch_page without reloading

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
    st.session_state['money'] = 100         #Start with 100 Euros


#EDIT THESE
#Text array
moneyThreshold = 20
optionsDict = {"Blue Hat": 10, "Red Hat": 30, "Brown Coat": 40, "Black Coat": 30, "White Shoes": 40, "Orange Shoes": 30}
print("Current choice: " + str(st.session_state['currentChoice']))
texts = ["Let’s go clothes shopping!", "You have €100. You need to have at least €20 for groceries after your clothes shopping", "First, let’s buy a new hat!", "There are 2 hats. The blue hat costs €10. The red hat costs €30.", "Which hat do you want to buy?", "Great! You bought the " + str(st.session_state['currentChoice']) + " ! You now have €" + str(st.session_state['money']) + " .", "Let’s continue with the clothes shopping.", "Let’s buy a new coat!", "There are 2 coats. The brown coat costs €40. The black coat costs €30.", "Which coat do you want to buy?", "Great! You bought the ____ coat! You now have €____.", "Let’s continue with the clothes shopping.", "Let’s buy new shoes!", "There are 2 pairs of shoes. The white shoes cost €40. The orange shoes cost €30.", "Which pair of shoes do you want to buy?", "Good job! You still have €20 after your clothes shopping!"]
print("Texts length")
print(len(texts))

st.header("Quest")
st.subheader("Clothes shopping")

colT1,colT2 = st.columns([0.25,0.75])
with colT2:
    #st.image("hats.png", width=256)

    colTT1,colTT2 = st.columns([0.4,0.6])
    with colTT1:
        print("cat")
        #st.image("cat.png", width=64)
    with colTT2:
        st.write("€"+str(st.session_state['money']))
    
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
        st.button(str(key1), use_container_width=True, on_click=changeText2, args=[key1, value1])
            
    with colT2:
        st.button(str(key2), use_container_width=True, on_click=changeText2, args=[key2, value2])

def navButtons(back, forward):
    #Use columns
    if back and forward:
        colT1,colT2 = st.columns(2)
        with colT1:

            #content = """<p><a href='#' id='Link 1'>First link</a></p>
            #<p><a href='#' id='Link 2'>Second link</a></p>
            #<a href='#' id='Image 1'><img width='20%' src='https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=200'></a>
            #<a href='#' id='Image 2'><img width='20%' src='https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=200'></a>
            #"""
            #clicked = click_detector(content)

            #st.markdown(f"**{clicked} clicked**" if clicked != "" else "**No click**")



            st.button("<-", use_container_width=True, on_click=changeText, args=['Back'], type="primary")
        with colT2:
            st.button("->", use_container_width=True, on_click=changeText, args=['Forward'], type="primary")
    
    #Dont use columns
    elif back:
        st.button("<-", use_container_width=True, on_click=changeText, args=['Back'], type="primary")
    elif forward:
        st.button("->", use_container_width=True, on_click=changeText, args=['Forward'], type="primary")

#UI
with st.container():
    st.text_area("Text", value=st.session_state['text'], label_visibility="collapsed")
    
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
            if st.button("Try again", use_container_width=True, type="primary"):
                st.session_state['text'] = 'Let’s go clothes shopping!'
                st.session_state['counter'] = 0
                st.session_state['oldCounter'] = 0
                st.session_state['currentChoice'] = ""
                st.session_state['money'] = 100
                st.rerun()
        print("END")
    #elif (st.session_state['counter'] > len(texts)):
    #    print("--------------------END-------------------")
    else:
        navButtons(True, True)
