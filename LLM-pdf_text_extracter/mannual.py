import streamlit as st
import pdfplumber
import openai

# Set your OpenAI API key
openai.api_key = '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'

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        all_text = ''
        for page in pdf.pages:
            all_text += page.extract_text()
    return all_text

# Function to summarize text with GPT-3
def summarize_text_with_gpt3(text):
    response = openai.Completion.create(
        model="text-davinci-004",
        prompt=f"Summarize the following text:\n{text}",
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()
# Tax calculation function
def calculate_tax(income, age, investment, loan, us_investment):
    # Define tax brackets and rates
    tax_brackets = [
        (500000, 0.1),    # 10% tax rate for income up to 5,00,001
        (1000000, 0.15),   # 15% tax rate for income between 10,00,001 and 5,00,000
        (2000000, 0.2),   # 20% tax rate for income between 10,00,001 and 20,00,000
        (3000000, 0.25),  # 25% tax rate for income between 20,00,001 and 30,00,000
        (5000000, 0.3),   # 30% tax rate for income between 30,00,001 and 50,00,000
        (float('inf'), 0.35)  # 35% tax rate for income above 50,00,000
    ]
    
    # Calculate taxable income
    taxable_income = income - investment - loan - us_investment
    
    # Calculate tax based on tax brackets
    tax = 0
    for bracket, rate in tax_brackets:
        if taxable_income <= 0:
            break
        if taxable_income <= bracket:
            tax += taxable_income * rate
            break
        else:
            tax += bracket * rate
            taxable_income -= bracket
    
    # Apply tax credits for senior citizens
    if age >= 60:
        tax *= 0.9  # 10% tax credit for senior citizens
    
    return tax

# Function to generate investment suggestions based on input data
def generate_suggestions(income, age, investment):
    suggestions = []
    
    # Suggestions for High Net Worth Individuals (HNIs)
    if income > 10000000:  # Example threshold for HNIs
        suggestions.append('Explore alternative investments such as venture capital, private equity, or hedge funds for higher returns.')
        suggestions.append('Consider offshore investments for diversification and tax optimization.')
    
    # Suggestions for Salaried Individuals
    if income < 500000:  # Example threshold for salaried individuals
        suggestions.append('Invest in tax-saving fixed deposits or Public Provident Fund (PPF) for tax benefits.')
        suggestions.append('Consider recurring deposits for short-term savings goals.')
    elif 500000 <= income < 1000000:
        suggestions.append('Explore mutual funds with a mix of equity and debt for balanced returns.')
        suggestions.append('Consider investing in Employee Provident Fund (EPF) or Voluntary Provident Fund (VPF) for retirement planning.')
    else:
        suggestions.append('Diversify your portfolio with a combination of mutual funds, stocks, and fixed-income instruments.')
        suggestions.append('Consider investing in Sovereign Gold Bonds (SGBs) for portfolio diversification and hedge against inflation.')
    
    # Suggestions for Other Individuals
    if age < 40:
        suggestions.append('Start building an emergency fund with a high-interest savings account or liquid funds.')
    elif 40 <= age < 60:
        suggestions.append('Review your insurance coverage and consider purchasing term insurance or health insurance if not already done.')
    else:
        suggestions.append('Focus on capital preservation and invest in low-risk instruments such as government bonds or Senior Citizens Savings Scheme (SCSS).')
    
    # Suggestions based on investment amount
    if investment < 50000:
        suggestions.append('Increase your investment amount to achieve financial goals faster.')
    elif 50000 <= investment < 100000:
        suggestions.append('Explore debt mutual funds or corporate bonds for stable returns with moderate risk.')
    else:
        suggestions.append('Consider real estate investments for long-term wealth creation and portfolio diversification.')
    
    return suggestions



def mannual():
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
        loan = st.number_input('Enter your loan amount:', min_value=0)
        us_investment = st.number_input('Enter your US investment amount:', min_value=0)
        submit_button = st.form_submit_button(label='Calculate Tax')

    if submit_button:
        tax = calculate_tax(income, age, investment, loan, us_investment)
        st.write('Your calculated tax:', tax)
        # Here you can add your investment suggestions logic
        suggestions = generate_suggestions(income, age, investment)
        st.header('Investment Suggestions')
        if suggestions:
            for suggestion in suggestions:
                st.write('- ', suggestion)
        else:
            st.write('No specific suggestions based on the provided data.')

    # Sidebar and footers
    st.sidebar.title('Contents')
    st.sidebar.write('[Home](#)')
    st.sidebar.write('[Tax Calculator](#tax)')
    st.sidebar.write('[Investment Suggestions](#suggestions)')
    st.sidebar.write('[About Us](#about)')
    st.markdown('---')
    st.write('Core Dump Team© 2024')

    # Detailed suggestions for tax reduction
    st.header('Tax Reduction Suggestions')
    st.subheader('1. Utilize Tax-Advantaged Accounts')
    st.write('Consider contributing to retirement accounts such as 401(k), IRA, or HSA to reduce taxable income.')

    st.subheader('2. Take Advantage of Tax Deductions and Credits')
    st.write('Explore available deductions and credits such as mortgage interest deduction, education expenses, or charitable donations.')

    st.subheader('3. Invest in Tax-Efficient Funds')
    st.write('Invest in funds that are tax-efficient, such as index funds or municipal bonds, to minimize tax obligations.')

    st.subheader('4. Harvest Tax Losses')
    st.write('Strategically sell investments to realize losses, which can offset capital gains and reduce taxable income.')

    st.subheader('5. Plan Charitable Contributions')
    st.write('Donate appreciated assets directly to charities to avoid capital gains taxes and receive tax deductions.')

    # Anchor links for sidebar
    st.write('<a name="tax"></a>', unsafe_allow_html=True)
    st.write('<a name="suggestions"></a>', unsafe_allow_html=True)
    st.write('<a name="about"></a>', unsafe_allow_html=True)
