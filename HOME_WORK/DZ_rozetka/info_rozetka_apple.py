from pprint import pprint
import sqlite3
import requests
from bs4 import BeautifulSoup


URL = "https://rozetka.com.ua/ua/promo/falldiscounts/?gad_campaignid=22015516959&gad_source=1&gbraid=0AAAAAq0EKAPQpSITO7IceX2J6dlJb2g7d&producer=apple&section_id=80003"

try:
    response = requests.get(URL)
    response.raise_for_status()
    html_content = response.text
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    exit()


soup = BeautifulSoup(html_content, "html.parser")

apple = soup.find_all("span", class_="goods-tile__title")
all_apple = []
for i in apple:
    all_apple.append(i.text.strip())

old_price = soup.find_all("div", class_="goods-tile__price--old price--gray")
all_old_price = []
for i in old_price:
    pr = i.text.strip()
    pr = pr.replace("\xa0", "")
    all_old_price.append(pr)

new_price = soup.find_all("span", class_="goods-tile__price-value")
all_new_price = []
for i in new_price:
    pr = i.text.strip()
    pr = pr.replace("\xa0", "")
    all_new_price.append(pr)

bonus = soup.find_all("p", class_="bonuses")
all_bonus = []
for i in bonus:
    bon = i.text.strip()
    bon = bon.replace("\xa0", "")
    all_bonus.append(bon)

combined_products = list(zip(all_apple, all_old_price, all_new_price, all_bonus))
pprint(combined_products)

connection = sqlite3.connect("users_data_sql3.db")
cursor = connection.cursor()
cursor.execute("""
    create table if not exists phones_apple (
    id integer primary key autoincrement,
    phone_model text not null,
    old_price text,
    new_price text,
    bonus text
);
""")
for i in combined_products:
    cursor.execute("""insert into phones_apple (phone_model, old_price, new_price, bonus)
     values (?, ?, ?, ?)""", i)
connection.commit()
connection.close()
