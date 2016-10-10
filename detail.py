import requests
from bs4 import BeautifulSoup

url = 'https://www.olx.com.pk/item/civic-87gl-a-cng-cleared-IDUIaEZ.html#8dc446e009'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

r = requests.get(url, headers=headers)

# make sure that the page exist

if r.status_code == 200:
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1')
    if title is not None:
        title_text = title.text.strip()

    location = soup.find('strong', {'class': 'c2b small'})
    if location is not None:
        location_text = location.text.strip()

    price = soup.select('div > .xxxx-large')
    if price is not None:
        price_text = price[0].text.strip('Rs').replace(',', '')

    images = soup.select('#bigGallery > li > a')
    img = [image['href'].strip() for image in images]

    description = soup.select('#textContent > p')
    if description is not None:
        description_text = description[0].text.strip()

# Creating a dictionary Object
item = {}
item['title'] = title_text
item['description'] = description_text
item['location'] = location_text
item['price'] = price_text
item['images'] = img

print(item)
