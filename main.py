import streamlit as st
from scraper import scrape_reviews, format_reviews
from utils import format_amazon_url

st.set_page_config(page_title="Amazon Review Scraper", page_icon="📚", layout="wide")

st.title("Amazon Review Scraper")

st.markdown("""
<style>
    .stTextInput>div>div>input {
        color: #4F8BF9;
    }
    .stButton>button {
        color: #4F8BF9;
        border-radius: 20px;
        height: 3em;
        width: 200px;
    }
    .stTextArea>div>div>textarea {
        color: #4F8BF9;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    url = st.text_input("Enter Amazon product URL:", placeholder="https://www.amazon.in/product/...")

with col2:
    num_reviews = st.number_input("Number of reviews to scrape:", min_value=1, max_value=100, value=10)

if st.button("Scrape Reviews"):
    if url:
        try:
            formatted_url = format_amazon_url(url)
            with st.spinner("Scraping reviews... This may take a few moments."):
                reviews = scrape_reviews(formatted_url, num_reviews)
                formatted_reviews = format_reviews(reviews)
            
            st.success(f"Successfully scraped {len(reviews)} reviews!")
            st.text_area("Scraped Reviews:", value=formatted_reviews, height=400)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a valid Amazon product URL.")

st.markdown("---")
