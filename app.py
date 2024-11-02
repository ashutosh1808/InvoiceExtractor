from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
from PIL import Image

#load all envs
load_dotenv()

#configure api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#gemini pro vision function
def get_gemini_content(input_prompt,image,question):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([input_prompt,image[0],question])
    return response.text

#input img details
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("Please upload an image")

#setup streamlit app
st.title("Invoice Extractor")
qn=st.text_input("What do you want to know?",key="input")

uploaded_image=st.file_uploader("Upload the invoice image",type=["jpg","jpeg","png"])
submit=st.button("Get details")
if uploaded_image is not None:
    image=Image.open(uploaded_image)
    st.image(image,use_column_width=True,caption="Uploaded invoice")

#if input and submit
input_prompt="""
You are an expert invoice analyst with knowledge about analysing and getting the detauls of
invoices of all the languages. Your job is to answer the question asked by the user about 
the invoice, which goes like
"""
if submit:
    image_info=input_image_details(uploaded_image)
    response=get_gemini_content(input_prompt,image_info,qn)
    st.subheader("Your response is")
    st.write(response)