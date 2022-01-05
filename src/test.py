from requests import get
from bs4 import BeautifulSoup

class Bot:

    def __init__(self, url):
        self.url = url

    def get_markup_content(self):
        page = get(self.url)
        html_soup = BeautifulSoup(page.text, 'html.parser')
        return html_soup.prettify()

bc = Bot(input())
with open("response.txt" ,"w") as file:
    file.write(bc.get_markup_content())