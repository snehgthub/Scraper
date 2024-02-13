import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

load_dotenv()

apiKey = os.getenv('APIKEY')
basetargetUrl = 'https://www.amazon.in'
endpointWithQuery = '/s?k=iphone+15&page='
scraperUrl = 'http://api.scraperapi.com'

for page in tqdm(range(1,4), desc='Downloading Content'):
    payload = {
    'api_key': apiKey,
    'url':  basetargetUrl+endpointWithQuery+str(page)
    }
    
    response = requests.get(scraperUrl, params=payload)
    soup = BeautifulSoup(response.content, 'html.parser')

    with open(f"html-amazon/amazon-{page}.html", 'w') as f:
        f.write(soup.prettify())
