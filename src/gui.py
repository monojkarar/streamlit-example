__version__ = "0.4.8.3"
app_name = "Ask my PDF"

# IMPORTS
import main
import streamlit as st
import time
import css
from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import (TextGenerationModel, CodeGenerationModel,
                                              ChatModel, InputOutputTextPair, ChatSession)
import vertexai
import json
from PIL import Image

# BOILERPLATE
st.set_page_config(layout='centered', page_title=f'{app_name} {__version__}')
# ss = st.session_state
# Initialization
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# Session State also supports attribute based syntax
if 'key' not in st.session_state:
    st.session_state.key = 'value'
ss = st.session_state

if 'debug' not in ss:
    ss['debug'] = {}

st.write(f'<style>{css.v1}</style>', unsafe_allow_html=True)
# header1 = st.empty()  # for errors / messages
# header2 = st.empty()  # for errors / messages
# header3 = st.empty()  # for errors / messages


# Initialize Vertex AI with the required variables
PROJECT_ID = 'team-11-lifesight-hack'
LOCATION = 'us-central1'
vertexai.init(project=PROJECT_ID, location=LOCATION)

if 'step' not in st.session_state:
    st.session_state.step = 0

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

questions = ['Please provide your name', 'Please provide your age', 'Please provide your gender, eg: As Male/Female',
             'If you want to share your health test details, eg: HbA1c=6. Once you are shared all the test details, type DONE',
             # 'Are you looking Diet Plan?', 'Are you looking for Workout & Exercises?',
             # 'Are you looking for Lifestyle suggestions?', 'Are you looking for Medicines & Drugs?',
             # 'Are you looking for Health Supplements?'
             ]
answers = []

prompt_questions = {}


# HANDLERS
def index_pdf_file():
    if ss['pdf_file']:
        ss['filename'] = ss['pdf_file'].name
        if ss['filename'] != ss.get('fielname_done'):  # UGLY
            with st.spinner(f'indexing {ss["filename"]}'):
                # index = model.index_file(ss['pdf_file'], ss['filename'], fix_text=ss['fix_text'],
                #                          frag_size=ss['frag_size'], cache=ss['cache'])
                # ss['index'] = index
                # debug_index()
                ss['filename_done'] = ss['filename']  # UGLY


def file_save():
    db = ss.get('storage')


def ui_pdf_file():
    st.markdown(
        f"""
            <style>
                body {{
                    background-color: #F5F5F5;
                }}
            </style>
            """,
        unsafe_allow_html=True
    )
    genre = st.radio(
        "How would you like to share your health report with us",
        ('UPLOAD', 'ADD PATIENT DETAILS'))

    if genre == 'UPLOAD':
        st.write('## Upload or select your XLSX file')
        uploaded_file = st.file_uploader('pdf file', type='xlsx', key='pdf_file',
                                         on_change=index_pdf_file, label_visibility="collapsed")
        st.session_state.uploaded_file = uploaded_file
        st.divider()
        if uploaded_file:
            with st.spinner('Wait for it...'):
                response = main.get_reports_multiple_patients(uploaded_file)
                time.sleep(1)
            data = json.loads(response)
            st.header(data["name"] + " | " + data["age"] + " years old.")
            st.divider()
            plans = data["plan"]
            index = 0
            for plan_id in plans:
                print(plan_id, '\n', plans[plan_id])
                st.title(plan_id)
                image = Image.open('images/' + str(index) + '.jpeg')
                st.image(image)
                st.info(plans[plan_id])
                st.divider()
                index = index + 1
    else:
        chat_prompt = st.chat_input("Say something")
        try:
            if chat_prompt:
                if chat_prompt.lower() == 'done':
                    for author, message in st.session_state.chat_history:
                        if author == "You":
                            answers.append(message)


                else:
                    # For this demo, let's create a dummy bot reply
                    st.session_state.chat_history.append(("Bot", f"{questions[st.session_state.step]}"))
                    # Append user's message to chat history
                    st.session_state.chat_history.append(("You", f"{chat_prompt}"))
                    # Clear the input box after sending a message
                for author, message in st.session_state.chat_history:
                    if author == "Bot":
                        st.warning(f"{message}")
                    else:
                        st.success(f"{message}")
                if len(chat_prompt.strip()) > 0 or chat_prompt == ' ' and st.session_state.step != 3:
                    st.session_state.step += 1
        except Exception as e:
            st.error(f"An error occurred: {e}")
        # if st.session_state.step == 2:
        if st.session_state.step < len(questions):
            st.warning(f"{questions[st.session_state.step]}")
        # else:
        #     st.write(f"{questions[st.session_state.step]}")
        # st.divider()

    # st.write('## Upload or select your PDF file')
    # tabs = st.tabs(['UPLOAD', 'ADD PATIENT DETAILS'])
    # with tabs[0]:
    #     uploaded_file = st.file_uploader('pdf file', type='pdf', key='pdf_file',
    #                                      on_change=index_pdf_file, label_visibility="collapsed")
    #     st.session_state.uploaded_file = uploaded_file
    #     st.divider()
    #     if uploaded_file:
    #         with open('data.json', 'r') as file:
    #             data = json.load(file)
    #             st.header(data["name"] + " | " + data["age"] + " years old.")
    #             st.divider()
    #             plans = data["plan"]
    #             index = 0
    #             for plan_id in plans:
    #                 print(plan_id, '\n', plans[plan_id])
    #                 st.title(plan_id)
    #                 image = Image.open('images/' + str(index) + '.jpeg')
    #                 st.image(image)
    #                 st.info(plans[plan_id])
    #                 st.divider()
    #                 index = index + 1
    # with tabs[1]:
    # chat_model = ChatModel.from_pretrained("chat-bison@001")
    # parameters = {
    #     "temperature": 0.2,  # Temperature controls the degree of randomness in token selection.
    #     "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    #     "top_p": 0.95,
    #     "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    # }
    # chat_prompt = st.chat_input("Say something")
    # print('Prompted Text =>', chat_prompt)
    # try:
    #     if chat_prompt:
    #         st.write(f"User has sent the following prompt: {chat_prompt}")
    #         chat = chat_model.start_chat()
    #         response = chat.send_message(
    #             chat_prompt, **parameters
    #         )
    #         print('Response =>', response)
    #         # st.success(response)
    #         st.write(response.text)
    # except Exception as e:
    #     st.error(f"An error occurred: {e}")
    # ui_text_prompt()
    # st.divider()


# def ui_text_prompt():
#     chat_model = ChatModel.from_pretrained("chat-bison@001")
#     parameters = {
#         "temperature": 0.2,  # Temperature controls the degree of randomness in token selection.
#         "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
#         "top_p": 0.95,
#         "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
#     }
#     prompt = st.chat_input("Say something")
#     print('Prompted Text =>', prompt)
#     try:
#         if prompt:
#             st.write(f"User has sent the following prompt: {prompt}")
#             chat = chat_model.start_chat()
#             response = chat.send_message(
#                 prompt, **parameters
#             )
#             print('Response =>', response)
#             # st.success(response)
#             st.write(response.text)
#     except Exception as e:
#         st.error(f"An error occurred: {e}")


ui_pdf_file()
# ui_text_prompt()
