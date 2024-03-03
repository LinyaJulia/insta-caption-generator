import streamlit as st
from dotenv import load_dotenv
from htmlTemplates import css
import numpy as np
from openai import OpenAI
import time
import pandas as pd

### https://inflact.com/tutorial/caption-copywriting/
### Reference

def generate_response(purpose):
    user_message_content = purpose

    response = st.session_state.openai_client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "You are an expert script social media copywriter tasked with coming up with instagram caption ideas based on a description of a purpose."
        },
        {
        "role": "user",
        "content": user_message_content
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response.choices[0].message.content  

def stream_data(text):
    for line in text.splitlines():
        for word in line.split():
            yield word + " "
            time.sleep(0.02)
        yield "\n"  # Add a new line after processing each line of text


def main():
    # load dotenv
    load_dotenv()

    # page config
    st.set_page_config(page_title="Instagram Caption Generator",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    # set api key
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = None

    st.title("Instagram Caption Generator")
    st.markdown("Put instructions here. Click on like.. the sidebar. You have to like add the api key. And then put your purpose and upload some files. Then press generate.")

    with st.sidebar:
        openai_key = st.text_input(
                "OpenAI API Key", 
                key="Open AI Api Key", 
                help="To use this app, you will need to have an OpenAI API Key. Access it from this link: https://platform.openai.com/account/api-keys")
        if openai_key:
            st.session_state.api_key = openai_key
            st.session_state.openai_client = OpenAI(api_key=st.session_state.api_key)
            


    purpose = st.text_area(
        "Purpose",
        help="In this input, indicate what sort of social media posts you want to make."
        )
    image_description = st.text_area(
        "Image Description",
        help="Describe the image you're posting..."
        )

    brand_guidelines = st.file_uploader(
        "Upload Brand Guidelines", 
        help="Make sure to follow these instructions for the brand guidelines to get the best results: link"
        )

    generate_btn = st.button(
        "Generate posts", 
        type="primary",
        use_container_width=True
        )
        
    st.divider()

    if generate_btn:

        user_message_content = (
        f"Here is the purpose of the post: {purpose}\n"
        f"Here is an image description: {image_description}\n"
        f"When making the post, please follow these brand guidelines: {brand_guidelines}\n"
        )

        with st.spinner("Processing"):
            st.write_stream(stream_data(generate_response(user_message_content))) 
        # ok, what happens when you click the button
        # you take purpose, image description, and brand guidelines
        # you send it to open ai chat something
        # get response
        # write response

        



if __name__ == '__main__':
    main()