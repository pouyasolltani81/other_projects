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


def scrape_and_save_product(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        
        random_delay(2, 5)

      
        soup = BeautifulSoup(driver.page_source, 'html.parser')

       
        script = soup.find('script', {'type': 'application/ld+json'})
        json_data = script.string

        data = json.loads(json_data)

        name = data.get('name')
        price = data.get('offers').get('price')
        # description = data.get('description')
        description = soup.find('article', class_ = 'lg:mt-4 px-5 lg:px-0 pb-5 styles_PdpProductContent__sectionBorder__39zAX')
        if description :
            description = description.get_text()
        else :
            description = data.get('description')


        list_info = soup.find('div', class_ = 'flex flex-col lg:flex-row pb-6 lg:py-4 styles_SpecificationBox__main__JKiKI')
        if list_info :
            list_info = list_info.get_text(separator=' | ')
        
        image_url = data.get('image')[0]

        driver.quit()


        finished_json = {
            'name': name,
            'description': description,
            'price': price,
            'image_url': image_url,
            'product_url': url,
            'list_info' : list_info,
            'header_json' : json_data
        }

       
        product_data = {
            'name': name,
            'description': description,
            'price': price,
            'image_url': image_url,
            'product_url': url,
        }

        # Save the product to the database
        Product.objects.create(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            image_url=product_data['image_url'],
            product_url=product_data['product_url'],
            json_data=json.dumps(finished_json)  
        )
        
        return product_data  

    except Exception as e:
        
        print(f"An error occurred: {e}")
        return None, str(e) 
