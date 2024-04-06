import streamlit as st

# Import your pages
from textReader import textReader as textReader_main
from mannual import mannual as mannual_main

# Main app
def main():
    # Create a sidebar with navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Text", "Mannual"])

    # Display the selected page
    if page == "Home":
        st.title("Home")
        st.write("Welcome to the TaxCaft. Use radio button at the left sidebar to toggle between the pages.")
    elif page == "Text":
        textReader_main()
    elif page == "Mannual":
        mannual_main()

    # Add toggle button to switch between text and mannual pages
    if page in ["Text", "Mannual"]:
        with st.sidebar.expander("Toggle between pages"):
            if page == "Text":
                st.write("Switch to Mannual")
                if st.button("Go to Mannual"):
                    st.experimental_rerun()
            elif page == "Mannual":
                st.write("Switch to Text")
                if st.button("Go to Text"):
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
