from bs4 import BeautifulSoup
import requests
from services import PoemsService, UsersService

# webscraping z strony wywrota.pl i poezja.org

file = open('links_to_poems').read()
links = file.split('\n')

service = PoemsService()
token = UsersService().login('admin', '12345')
count = 1

for url in links:
    if url != '':
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        if 'literatura.wywrota.pl' in url:
            for span_tag in soup.findAll('span'):
                span_tag.replace_with('')
            title = soup.find('h1', class_='textTitle').text.strip()
            author = soup.find('h2', class_='autor').text.strip()
            content = soup.find_all('div', class_="txtcore")[1].text.strip()
        elif 'poezja.org' in url:
            title = soup.find('div', class_='col-12 col-lg-8').text.strip()
            author = soup.find('a', class_='author').text.strip()
            content = soup.find_all('div', class_='col-12 col-lg-8')[2].find('p')
            for p in content.findAll('p'):
                p.replace_with('')
            content = content.text.strip()
        try:
            print(f'{count}. {author}: {title}')
            service.addPoem(token, author, title, content)
        except Exception as e:
            print(e)

        count += 1
