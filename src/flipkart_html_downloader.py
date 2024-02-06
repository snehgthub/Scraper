import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

apiKey = os.getenv('APIKEY')

baseTargetUrl = 'https://www.flipkart.com'
endpointWithQuery = '/search?q=iphone+15'
pageQuery = '&page='
scraperUrl = 'http://api.scraperapi.com'
platform = 'flipkart'

for page in tqdm(range(1,4), desc='Downloading content:'):
    payload = {
        'api_key': apiKey,
        'url': baseTargetUrl+endpointWithQuery+pageQuery+str(page)
    }

    response = requests.get(scraperUrl, params=payload)
    soup = BeautifulSoup(response.content, 'html.parser')

    with open(f"html/{platform}-{page}.html", 'w') as fp:
        fp.write(soup.prettify())