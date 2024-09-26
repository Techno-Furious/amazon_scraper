import streamlit as st
from scraper import scrape_reviews
from utils import format_amazon_url

st.set_page_config(page_title="Amazon Review Scraper", page_icon="📚", layout="wide")

st.title("Amazon Review Scraper")

url = st.text_input("Enter Amazon product URL:", placeholder="https://www.amazon.in/product/...")

num_reviews = st.number_input("Number of reviews to scrape:", min_value=1, max_value=100, value=10)

if st.button("Scrape Reviews"):
    if url:
        formatted_url = format_amazon_url(url)
        with st.spinner("Scraping reviews..."):
            df,reviews = scrape_reviews(formatted_url, num_reviews)
            if reviews:
                st.success(f"Successfully scraped {len(reviews)} reviews!")
                st.dataframe(df)
            else:
                st.error("Failed to scrape reviews.")
    else:
        st.warning("Please enter a valid Amazon product URL.")
