import requests
from bs4 import BeautifulSoup
url = "https://www.resultadobaloto.com/"
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
for i, t in enumerate(soup.find_all('table')[:2]):
    print(f"Table {i}:")
    for r in t.find_all('tr'):
        cols = [c.text.strip() for c in r.find_all(['th','td'])]
        print(" | ".join(cols))
