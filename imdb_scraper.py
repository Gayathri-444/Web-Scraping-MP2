from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re

driver_path = r"C:\Users\gayat\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Start driver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

print("🔄 Loading IMDb Top 250 page (Headless Mode)...")
driver.get("https://www.imdb.com/chart/top")

time.sleep(8)

movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

titles, years, ratings = [], [], []

for movie in movies:
    try:
        title_raw = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
        title = re.sub(r"^\d+\.\s*", "", title_raw)

        year = movie.find_element(By.CSS_SELECTOR, "span.cli-title-metadata-item").text
        rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text

        titles.append(title)
        years.append(year)
        ratings.append(rating)
    except Exception:
        continue

# Create CSV
df = pd.DataFrame({
    "Movie Title": titles,
    "Release Year": years,
    "IMDb Rating": ratings
})

df.to_csv("imdb_top_250.csv", index=False)
df.to_csv("imdb_top_250.csv", index=False)

print(f"✅ Successfully scraped {len(df)} movies in headless mode!")
print("📁 Clean file saved as 'imdb_top_250.csv'")

driver.quit()
