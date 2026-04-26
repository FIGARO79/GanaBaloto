import requests
from bs4 import BeautifulSoup

url = "https://www.resultadobaloto.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Print some of the HTML around Baloto
secciones = soup.find_all(lambda tag: tag.name in ["h2", "h1", "div"] and "Baloto" in tag.text)
for s in secciones[:5]:
    print(f"Tag: {s.name}, Text snippet: {s.text[:50]}")
    parent = s.find_parent('div')
    print(f"Parent div found: {parent is not None}")
    if parent:
        print(f"Parent classes: {parent.get('class')}")
        # Show children
        for child in parent.find_all(recursive=False):
            print(f"  Child: {child.name}, class: {child.get('class')}")

# Specifically look for anything that looks like a ball
balls = soup.find_all(class_=lambda x: x and ('ball' in x.lower() or 'numero' in x.lower()))
print(f"\nFound {len(balls)} elements with 'ball' or 'numero' in class")
for b in balls[:10]:
    print(f"Tag: {b.name}, Class: {b.get('class')}, Text: {b.text.strip()}")
