import streamlit as st
import pdfplumber
import openai

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        all_text = ''
        for page in pdf.pages:
            all_text += page.extract_text()
    return all_text

# Function to summarize text using GPT-3
def summarize_text_with_gpt3(text):
    openai.api_key = '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'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following text:\n{text}",
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Streamlit app
st.title('TaxCraft')

# Upload PDF and extract text
st.header('Upload Your Tax Document')
uploaded_file = st.file_uploader('Choose a file', type=['pdf', 'docx'])

if uploaded_file is not None:
    extracted_text = extract_text_from_pdf(uploaded_file)
    summarized_text = summarize_text_with_gpt3(extracted_text)
    st.write('Summary of your document:', summarized_text)

# User input for tax information
st.header('Enter Your Tax Information')
with st.form(key='tax_form'):
    income = st.number_input('Enter your annual income:', min_value=0)
    age = st.number_input('Enter your age:', min_value=0, max_value=100)
    investment = st.number_input('Enter your investment amount:', min_value=0)
    submit_button = st.form_submit_button(label='Calculate Tax')

if submit_button:
    st.write('Your annual income:', income)
    st.write('Your age:', age)
    st.write('Your investment amount:', investment)
    # Here you can add your investment suggestions logic

# Sidebar and footer
st.sidebar.title('Contents')
st.sidebar.write('Home')
st.sidebar.write('Tax Calculator')
st.sidebar.write('Investment Suggestions')
st.sidebar.write('About Us')
st.markdown('---')
st.write('Core Dump Team© 2024')
