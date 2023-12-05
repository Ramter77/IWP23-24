import asyncio
import json
import sys
import base64
import requests
import sseclient
import os

import streamlit as st
import streamlit_chat
from st_clickable_images import clickable_images
from streamlit_extras.switch_page_button import switch_page

# For local streaming, the websockets are hosted without ssl - ws://
PORT = 7860     #default port
HOST = 'localhost:5005'

# For reverse-proxied streaming, the remote will likely host with ssl - wss://
# URI = 'wss://your-uri-here.trycloudflare.com/api/v1/stream'
URIprefixValue = "h-textbook-rpm-vegetation"

st.set_page_config(
    page_title="QuestChat",
    page_icon="👋",
    initial_sidebar_state="collapsed",
    #layout='wide'
)

with st.sidebar:
    #def updateURI():
    #    st.session_state.URIprefix = URIprefix.value
        #print("sdg")

    st.session_state.URIprefix = st.text_input(label="URI prefix", key="URIpre", placeholder="Input the URI prefix", help="The URI prefix")    #set uri prefix from textgenUI
    URI = f'https://{st.session_state.URIprefix}.trycloudflare.com/v1/chat/completions'     #add prefix to get complete URI
    temp = st.number_input("Temperature", value=0.1, help="Default 0.1")   #set low to get deterministic results
    #st.session_state.URIprefix = URIprefix.value

async def run(user_input, history, stream):
    history.append({"role": "user", "content": user_input})

    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        'mode': 'instruct',
        'stream': stream,
        'messages': history,
        'character': 'Petname',
        #'instruction_template': 'OpenChat',
        ##'your_name': 'You',

        ##'regenerate': False,
        ##'_continue': False,
        #'stop_at_newline': False,
        #'chat_prompt_size': 2048,
        #'chat_generation_attempts': 1,
        #'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',
        #'max_new_tokens': 250,
        #'do_sample': True,
        #'temperature': 1,
        #'top_p': 0.1,
        #'typical_p': 1,
        #'epsilon_cutoff': 0,  # In units of 1e-4
        #'eta_cutoff': 0,  # In units of 1e-4
        #'tfs': 1,
        #'top_a': 0,
        #'repetition_penalty': 1.18,
        #'top_k': 40,
        #'min_length': 0,
        #'no_repeat_ngram_size': 0,
        #'num_beams': 1,
        #'penalty_alpha': 0,
        #'length_penalty': 1,
        #'early_stopping': False,
        #'mirostat_mode': 0,
        #'mirostat_tau': 5,
        #'mirostat_eta': 0.1,
        #'seed': 1,
        #'add_bos_token': True,
        #'truncation_length': 2048,
        #'ban_eos_token': False,
        #'skip_special_tokens': True,
        #'stopping_strings': []
    }

    stream_response = requests.post(URI, headers=headers, json=data, verify=False, stream=True)
    client = sseclient.SSEClient(stream_response)

    #print(stream_response)
    if str(stream_response) != "<Response [200]>":
        st.error("Server down or not set correct URI")

    element = st.empty()
    assistant_message = ''
    for event in client.events():
        payload = json.loads(event.data)
        chunk = payload['choices'][0]['message']['content']
        assistant_message += chunk
        print(chunk, end='')
        sys.stdout.flush()  # If we don't flush, we won't see tokens in realtime.
        element.write(assistant_message)

    element.empty()
    history.append({"role": "assistant", "content": assistant_message})

    streamlit_chat.message(assistant_message)

    print()
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(history)
    return assistant_message

# be sure to end each prompt string with a comma.
example_user_prompts = [
    "echo Hello World!",
    "How old is Elon Musk?",
    "What makes a good joke?",
    "Tell me a haiku.",
]

def move_focus():
    # inspect the html to determine which control to specify to receive focus (e.g. text or textarea).
    st.components.v1.html(
        f"""
            <script>
                var textarea = window.parent.document.querySelectorAll("textarea[type=textarea]");
                for (var i = 0; i < textarea.length; ++i) {{
                    textarea[i].focus();
                }}
            </script>
        """,
    )

def complete_messages(nbegin,nend,stream=True):
    messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
    with st.spinner(f"Waiting for {nbegin}/{nend} responses..."):
        if stream:
            response_content = asyncio.run(run(st.session_state.messages[-1]['content'], messages, True))
            print(response_content)
        else:
            #response = openai.ChatCompletion.create(
            #    model=st.session_state["openai_model"],
            #    messages=[
            #        {"role": m["role"], "content": m["content"]}
            #        for m in st.session_state.messages
            #    ],
            #    stream=False,
            #)
            #response_content = response.choices[0]['message'].get("content","")
            response_content = asyncio.run(run(st.session_state.messages[-1]['content'], messages, False))
            print(response_content)
    return response_content

def chat():
    #if "openai_model" not in st.session_state:
    #    st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    #if "userid" in st.session_state:
    #st.sidebar.text_input(
    #    "Current userid", on_change=userid_change, placeholder=st.session_state.userid, key='userid_input')
    if st.sidebar.button("Clear Conversation", key='clear_chat_button'):
        st.session_state.messages = []
        move_focus()
    if st.sidebar.button("Show Example Conversation", key='show_example_conversation'):
        #st.session_state.messages = [] # don't clear current conversaations?
        for i,up in enumerate(example_user_prompts):
            st.session_state.messages.append({"role": "user", "content": up})
            assistant_content = complete_messages(i,len(example_user_prompts))
            st.session_state.messages.append({"role": "assistant", "content": assistant_content})
        move_focus()
    for i,message in enumerate(st.session_state.messages):
        nkey = int(i/2)
        if message["role"] == "user":
            streamlit_chat.message(message["content"], is_user=True, key='chat_messages_user_'+str(nkey))
        else:
            streamlit_chat.message(message["content"], is_user=False, key='chat_messages_assistant_'+str(nkey))

    if user_content := st.chat_input("Start typing..."): # using streamlit's st.chat_input because it stays put at bottom, chat.openai.com style.
            nkey = int(len(st.session_state.messages)/2)
            st.session_state.messages.append({"role": "user", "content": user_content})
            streamlit_chat.message(user_content, is_user=True, key='chat_messages_user_'+str(nkey))
            
            assistant_content = complete_messages(0,1)
            #st.session_state.messages.append({"role": "assistant", "content": assistant_content})
            streamlit_chat.message(assistant_content, key='chat_messages_assistant_'+str(nkey))
            
            print("-------------------------Messages---------------------")
            print(st.session_state.messages)
            #len(st.session_state.messages)
    #else:
    #    st.sidebar.text_input(
    #        "Enter a random userid", on_change=userid_change, placeholder='userid', key='userid_input')
    #    streamlit_chat.message("Hi. I'm your friendly streamlit ChatGPT assistant.",key='intro_message_1')
    #    streamlit_chat.message("To get started, enter a random userid in the left sidebar.",key='intro_message_2')

def stickHeader():
    st.markdown(
        """
            <div class='fixed-header'/>
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                    position: sticky;
                    top: 2.875rem;
                    z-index: 999;
                    float: right;
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
                padding-bottom: 120px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        gif_html = get_img_with_href()
        st.markdown(gif_html, unsafe_allow_html=True)

        stickHeader()

@st.cache_data()
def get_img_with_href():
    img_format = os.path.splitext('x.png')[-1].replace('.', '')
    bin_str = get_base64_of_bin_file('x.png')

    html_code = f'''
        <div class="container">
            <div class="cont" style="float:right; cursor:pointer; heigth:56px;">
                <a target="_self" href="{'/Home'}">
                    <img style="width= width="56px" height="56px" src="data:image/{img_format};base64,{bin_str}" />
                </a>
            </div>
        </div>'''
    return html_code

@st.cache_data()
def get_img_with_href2(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f"""
            <a href="{target_url}" style="float:right">
                <img width="56px" heigth="56px" src="data:image/{img_format};base64,{bin_str}" />
            </a>
            """
    return html_code

testPrompt = "I want you to act as a very simple text based adventure game with financial context for a target audience with minor cognitive impairments. Respond with a short and simple description of the environment and then ask me a short and simple question that can only be answered with yes or no. My first scenario is: “buy a hat”"

def main():
    if "URIprefix" not in st.session_state:
        st.session_state.URIprefix = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

    set_png_as_page_bg('chatBG.png')
    header()

    if st.button("Start Quest", use_container_width=True, type='primary'):
        asyncio.run(run(testPrompt, st.session_state.messages, True))
        #history.append({"role": "assistant", "content": assistant_message})


    col1, col2 = st.columns(2)
    ans = ''
    with col1:
        if st.button("Yes", use_container_width=True, type='primary'):
            ans = "Yes"
    with col2:
        if st.button("No", use_container_width=True, type='secondary'):
            ans = "No"

    if (ans == "Yes" or ans == "No"):
        asyncio.run(run("Continue the text based game. I choose: " + ans, st.session_state.messages, True))

if __name__ == '__main__':
    main()    