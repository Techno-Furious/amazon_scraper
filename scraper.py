from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import extract_rating, extract_place_and_date
import time

def scrape_reviews(url, num_reviews):
    chrome_options = Options()
    # Ensures no GUI is required and runs fully headless
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")  # Required for some cloud environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources in containers
    chrome_options.add_argument("--disable-gpu")  # Optional, if GPU issues occur
    chrome_options.add_argument("--window-size=1920x1080")  # Set the window size for consistency in headless mode
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    reviews = []
    page = 1

    while len(reviews) < num_reviews:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-hook='review']"))
        )

        review_elements = driver.find_elements(By.CSS_SELECTOR, "[data-hook='review']")

        for review in review_elements:
            if len(reviews) >= num_reviews:
                break

            try:
                rating_element = review.find_element(By.CSS_SELECTOR, "i[data-hook='review-star-rating']")
                rating_string = rating_element.get_attribute('innerHTML')
                rating = extract_rating(rating_string)

                title = review.find_element(By.CSS_SELECTOR, "a[data-hook='review-title']").text
                body = review.find_element(By.CSS_SELECTOR, "span[data-hook='review-body']").text
                date_string = review.find_element(By.CSS_SELECTOR, "span[data-hook='review-date']").text
                place, date = extract_place_and_date(date_string)
                
                reviews.append({
                    'rating': rating,
                    'title': title,
                    'body': body,
                    'place': place,
                    'date': date
                })
            except Exception as e:
                print(f"Error extracting review: {str(e)}")

        if len(reviews) < num_reviews:
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.a-last a")
                next_button.click()
                time.sleep(2)
                page += 1
            except Exception as e:
                print(f"Error navigating to next page: {str(e)}")
                break

    driver.quit()
    return reviews

def format_reviews(reviews):
    formatted_reviews = ""
    for review in reviews:
        formatted_reviews += f"Rating: {review['rating']}\n"
        formatted_reviews += f"Title: {review['title']}\n"
        formatted_reviews += f"Place: {review['place']}\n"
        formatted_reviews += f"Date: {review['date']}\n"
        formatted_reviews += f"Review: {review['body']}\n"
        formatted_reviews += "-" * 50 + "\n"
    return formatted_reviews