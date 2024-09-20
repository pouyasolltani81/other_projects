from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time
import random
from .models import Product



def random_delay(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))


def scrape_product(url):
    

    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")

    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

        
    
    random_delay(2, 5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    script = soup.find('script' , {'type':'application/ld+json'})

    json_data= script.string

    data = json.loads(json_data)

    name = data.get('name')

    
    price = data.get('offers').get('price')

    description = data.get('description')
    image_url = data.get('image')[0]


    driver.quit()
    
    Product.objects.create(
        name=name, 
        description=description, 
        price=price, 
        image_url=image_url, 
        product_url=url
    )
