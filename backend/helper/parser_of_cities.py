import requests
from bs4 import BeautifulSoup


def get_cities():
    url = "https://uk.wikipedia.org/wiki/Список_міст_України"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    cities = []
    table = soup.find('table', {'class': 'wikitable'})
    rows = table.find_all('tr')

    for row in rows[1:]:
        city_cell = row.find_all('td')[1]
        city_name = city_cell.text.strip()
        cities.append(city_name)

    return cities
