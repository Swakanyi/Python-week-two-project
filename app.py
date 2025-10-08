import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


api_key = "a34d6bb959-9006855c0b-t3nqf5"
base ="GBP"
target = "KES"
url = f"https://api.fastforex.io/fetch-one?from={base}&to={target}&api_key={api_key}"

#get request
response = requests.get(url)
if response.status_code == 200:
    convert_data = response.json()
    rate = convert_data['result'][target]
    print(f"{base} = {rate:.2f} {target}")

else:
    print("Error fetching conversion rate")
    rate = None


response = requests.get("https://books.toscrape.com/")
#print(response.content)

soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)

#EXTRACTING PRODUCT NAME & PRICE
data = []
books = soup.find_all('article', class_='product_pod')[:10]
for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    price_gbp = float(price.replace('£', '').strip())

    if rate:
        price_kes = price_gbp * rate
    else:
        price_kes = None

    data.append([title, f"£{price_gbp:.2f}", f"KES {price_kes:.2f}" if price_kes else "N/A"])
#print(data)  

#panda format
df = pd.DataFrame(data)
print(df.to_string(index=False))

#to store in .csv
file = open("books.csv", "w", encoding="utf-8")
writer = csv.writer(file)
writer.writerow(["Title", "Price (GBP)", "Price (KES)"])
writer.writerows(data)