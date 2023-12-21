import requests
from bs4 import BeautifulSoup
import pandas as pd

product_urls = [
    "https://www.walmart.com/ip/AT-T-iPhone-14-128GB-Midnight/1756765288",
    "https://www.walmart.com/ip/Straight-Talk-Apple-iPhone-14-Pro-12 8GB-Silver-Prepaid-Smartphone-Locked-to-Straight-Talk/1667543930"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

product_data = []

for url in product_urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("h1").text
    price = soup.find("span", {"itemprop": "price"}).text
    product_data.append({
        "title": title,
        "price": price,
    })

df = pd.DataFrame(columns=["title", "price"])
df = df.append(product_data)
df.to_csv("result.csv", index=False) 