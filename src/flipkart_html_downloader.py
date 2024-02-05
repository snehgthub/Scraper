import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv('APIKEY')

baseTargetUrl = 'https://www.flipkart.com'
endpointWithQuery = '/search?q=iphone+15'
scraperUrl = 'http://api.scraperapi.com'
platform = 'flipkart'

payload = {
    'api_key': apiKey,
    'url': baseTargetUrl+endpointWithQuery
}

response = requests.get(scraperUrl, params=payload)
soup = BeautifulSoup(response.content, 'html.parser')

with open(f"html/{platform}.html", 'w') as fp:
    fp.write(soup.prettify())