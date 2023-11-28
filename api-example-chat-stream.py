import asyncio
import json
import sys
import base64
from pathlib import Path
import streamlit as st
from st_click_detector import click_detector
from st_clickable_images import clickable_images
import requests
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import streamlit_chat
import audiorecorder

try:
    import websockets
except ImportError:
    print("Websockets package not found. Make sure it's installed.")

PORT = 7860     #default port
URIprefixValue = "briefing-coordinated-assists-achieving"

# For local streaming, the websockets are hosted without ssl - ws://
HOST = 'localhost:5005'
#URI = f'ws://{HOST}/api/v1/chat-stream'

# For reverse-proxied streaming, the remote will likely host with ssl - wss://
# URI = 'wss://your-uri-here.trycloudflare.com/api/v1/stream'

#UI
title = "Petname"
subtitle = "Daily motivational text"

st.set_page_config(
    page_title="Test",
    page_icon="👋",
    initial_sidebar_state="collapsed"
)

with st.sidebar:
    URIprefix = st.text_input(label="URI prefix", value=URIprefixValue, key="URIpre", placeholder="Input the URI prefix", help="The URI prefix")    #set uri prefix from textgenUI
    URI = f'wss://{URIprefix}.trycloudflare.com/api/v1/chat-stream'              #add prefix to get complete URI
    temp = st.number_input("Temperature", value=0.1, help="Default 0.1")        #set low to get deterministic results

def header():
    with st.container():
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.title(title)
            st.subheader(subtitle)
        with col2:
            st.image("pet.png", width=64)
            st.image("currency.png", width=64)
        stickHeader()

def footer():
    images = []
    for file in ["task.png", "home.png", "quests.png", "diary.png", "share.png"]:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")

    with st.container():
        clicked = clickable_images(
            images,
            #titles=[f"Image #{str(i)}" for i in range(2)],
            titles=["Tasks", "Home", "Quests", "Diary", "Share"],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "cursor": "pointer"},
            img_style={"margin": "5px", "width": "15.5%"},
            #img_style={"margin": "5px", "height": "200px"},
        )

        #print(clicked)
        if (clicked == 2):
            switch_page("Quests")

        audioRecord()
        stickFooter()

def audioRecord():  #AUDIO RECORDING
    audio = audiorecorder("Click to record audio", "Click to stop recording")
    if len(audio) > 0:
        st.audio(audio.export().read())     # To play audio in frontend:

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
                    bottom: 15%;
                    top: 28%;
                    text-color: white;
                    z-index: 999;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

async def run(user_input, history):
    # Note: the selected defaults change from time to time.
    request = {
        'user_input': user_input,
        'history': history,
        'mode': 'chat',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        'character': 'Petname',
        'instruction_template': 'WizardLM',
        'your_name': 'You',

        'regenerate': False,
        '_continue': False,
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

    async with websockets.connect(URI, ping_interval=None) as websocket:
        await websocket.send(json.dumps(request))

        while True:
            incoming_data = await websocket.recv()
            incoming_data = json.loads(incoming_data)

            if incoming_data['event'] == 'text_stream':
                yield incoming_data['history']
            elif incoming_data['event'] == 'stream_end':
                return


async def print_response_stream(user_input, history):
    element = st.empty()

    #print("PRINTING")
    cur_len = 0
    mess1 = []
    oldText = ''
    async for new_history in run(user_input, history):
        cur_message = new_history['visible'][-1][1][cur_len:]
        cur_len += len(cur_message)

        mess1.append(cur_message)
        mess = "".join(mess1)
        mess1.pop(0)

        print(cur_message, end='')
        sys.stdout.flush()  # If we don't flush, we won't see tokens in realtime.

        oldText += (mess)
        #element.chat_message(oldText)
        element.write(oldText)
    
    element.empty()
    return oldText

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

async def testt(history):
    result = await print_response_stream(st.session_state.messages[-1]['content'], history)
    return result
            

def complete_messages(nbegin,nend,stream=True):
    messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
    with st.spinner(f"Waiting for {nbegin}/{nend} responses..."):
        if stream:
            #user_input = "Please give me a step-by-step guide on how to plant a tree in my backyard."
            responses = []

            history = {'internal': [], 'visible': []}
            responses = asyncio.run(testt(history))
            print("zsddddddddddddddddddddddddddddddddddddddddd")
            print(responses)
            response_content = "".join(responses)
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
            #response_content = "test"
            #print(messages[0]['content'])
            history = {'internal': [], 'visible': []}
            print("Prompt: " + messages[0]['content'])
            response = run(messages[0]['content'], history)
            response_content = response
    return response_content

def chat2():
    #if "openai_model" not in st.session_state:
    #    st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    #with st.container():
    #    st.title("Streamlit ChatGPT Bot")
    #    stick_it_good()

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
            st.session_state.messages.append({"role": "assistant", "content": assistant_content})
            streamlit_chat.message(assistant_content, key='chat_messages_assistant_'+str(nkey))
            
            #len(st.session_state.messages)
    #else:
    #    st.sidebar.text_input(
    #        "Enter a random userid", on_change=userid_change, placeholder='userid', key='userid_input')
    #    streamlit_chat.message("Hi. I'm your friendly streamlit ChatGPT assistant.",key='intro_message_1')
    #    streamlit_chat.message("To get started, enter a random userid in the left sidebar.",key='intro_message_2')

def userid_change():
    st.session_state.userid = st.session_state.userid_input

if __name__ == '__main__':
    header()
    chat2()
    footer()