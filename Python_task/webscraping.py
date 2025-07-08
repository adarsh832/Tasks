import requests

url = "https://en.wikipedia.org/wiki/Hello_(Adele_song)" 
response = requests.get(url)
html_content = response.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
print(soup)     