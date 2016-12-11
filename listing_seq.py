import requests
from bs4 import BeautifulSoup
from time import sleep


def get_listing(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    html = None
    links = None
    try:
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            listing_section = soup.select('#offers_table table > tbody > tr > td > h3 > a')
            links = [link['href'].strip() for link in listing_section]
    except Exception as ex:
        print(str(ex))
    finally:
        return links


# parse a single item to get information
def parse(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    info = []
    title_text = '-'
    location_text = '-'
    price_text = '-'
    title_text = '-'
    images = '-'

    try:
        r = requests.get(url, headers=headers, timeout=10)
        sleep(2)

        if r.status_code == 200:
            print('Processing..' + url)
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
                price_text = price[0].text.strip('Rs').replace(',', '').replace('\n', '')

            images = soup.select('#bigGallery > li > a')
            img = [image['href'].replace('\n', '').strip() for image in images]
            images = '^'.join(img)

            info.append(url)
            info.append(title_text)
            info.append(location_text)
            info.append(price_text)
            info.append(images)
    except Exception as ex:
        print(str(ex))
    finally:
        if len(info) > 0:
            return ','.join(info)
        else:
            return None


car_links = None
cars_info = []
cars_links = get_listing('https://www.olx.com.pk/cars/')

[cars_info.append(parse(car_link)) for car_link in cars_links]
if len(cars_info) > 0:
    with open('data.csv', 'a+') as f:
        f.write('\n'.join(cars_info))
