import re

def format_amazon_url(url):
    # Extract ASIN from the URL
    asin_match = re.search(r'/([A-Z0-9]{10})(?:/|\?|$)', url)
    if not asin_match:
        raise ValueError("Invalid Amazon URL. Could not find ASIN.")
    asin = asin_match.group(1)

    # Construct the properly formatted URL
    formatted_url = f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=avp_only_reviews&sortBy=helpful&pageNumber=1"
    return formatted_url

def extract_rating(rating_string):
    match = re.search(r'(\d+(\.\d+)?)', rating_string)
    return float(match.group(1)) if match else None

def extract_place_and_date(date_string):
    match = re.match(r'Reviewed in (.*?) on (.*)', date_string)
    if match:
        return match.group(1), match.group(2)
    return None, None