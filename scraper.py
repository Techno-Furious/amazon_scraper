import requests
from selectorlib import Extractor
from dateutil import parser as dateparser
import pandas as pd

# Load the extractor from the YAML file
extractor = Extractor.from_yaml_file('selectors.yml')

def scrape_reviews(url, num_reviews):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'
    }

    reviews = []
    page = 1

    while len(reviews) < num_reviews:
        print(f"Scraping page {page} of reviews...")
        response = requests.get(url, headers=headers)
        
        if response.status_code > 500:
            if "automated access to Amazon data" in response.text:
                print("Blocked by Amazon. Try using a proxy or reducing request frequency.")
                return None
            print(f"Error {response.status_code}: Unable to fetch page.")
            break
        
        # Use selectorlib to extract data
        data = extractor.extract(response.text, base_url=url)
        
        if not data['reviews']:
            print("No reviews found.")
            break
        
        for r in data['reviews']:
            # Clean up and structure the data
            date_posted = r.get('date', '').split('on ')[-1]
            r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y') if date_posted else 'Unknown'

            # Check if the rating exists before processing
            rating = r.get('rating', None)
            if rating:
                try:
                    r['rating'] = float(r['rating'].split('out of')[0].strip())
                except (ValueError, AttributeError):
                    r['rating'] = None  # Handle the case where rating format is incorrect
            else:
                r['rating'] = None  # Set rating to None if not found
            
            # Check if 'verified_purchase' exists
            r['verified_purchase'] = 'Verified Purchase' in r.get('verified_purchase', '')

            # Handle 'found_helpful' safely
            found_helpful = r.get('found_helpful', '0')  # Default to '0' if None
            if found_helpful:
                found_helpful = found_helpful.split()[0]  # Split and take the first value if available
            else:
                found_helpful = '0'  # Fallback to '0'

            reviews.append({
                'author': r.get('author', 'Unknown'),
                'title': r.get('title', 'No Title'),
                'content': r.get('content', 'No Content'),
                'date': r['date'],
                'rating': r['rating'],
                'found_helpful': found_helpful,
                'verified_purchase': r['verified_purchase'],
                'variant': r.get('variant', ''),
                'product': data.get('product_title', ''),
                'url': url
            })
        
        # Stop if enough reviews are collected
        if len(reviews) >= num_reviews:
            break

        # Move to the next page if available
        next_page = data.get('next_page')
        if next_page:
            # Check if the URL already contains the full URL
            if next_page.startswith("http"):
                url = next_page  # Use the full URL if already provided
            else:
                url = f"https://www.amazon.in{next_page}"  # Concatenate correctly
            page += 1
        else:
            break
    df=pd.DataFrame(reviews)
    return df,reviews[:num_reviews]
