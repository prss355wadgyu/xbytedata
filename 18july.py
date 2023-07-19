import json
import requests
import mysql.connector
from datetime import datetime
from pyasn1_modules.rfc2315 import data

#Connect to mySql
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="xbyte"
)

#create table and columns
class Noon:
    def __init__(self):
        c = db.cursor()
        self.table_name = 'beauty_product'
        self.columns = {
            'sr_no': 'INT AUTO_INCREMENT PRIMARY KEY',
            'brand': 'VARCHAR(255)',
            'product_name': 'VARCHAR(255)',
            'price': 'INT',
            'old_price': 'VARCHAR(255)',
            'link': 'text',
            # 'image_link':'VARCHAR(255)',
            'rating':'VARCHAR(255)',
            'total_rating': 'VARCHAR(255)',
            'date_time':'varchar(255)'

        }

        column_definitions = ', '.join([f'{col} {self.columns[col]}' for col in self.columns])
        query = f'CREATE TABLE IF NOT EXISTS db3.{self.table_name} ({column_definitions})'
        c.execute(query)
        print("Table created successfully")


#loads jason
    def scrap(self,url,page,headers):
        response=requests.get(url=url, headers=headers)
        data=json.loads(response.text)

#Get data from hints
        hits = data.get('hits')
        for item in hits:
            brand = item.get('brand')
            name = item.get('name')
            price=item.get('price')
            old_price=item.get('sale_price')
            sku=item.get('sku')
            offer_code=item.get('offer_code')
            url1=item.get('url')
            link='https://www.noon.com/uae-en/'+ url1 + "/" + sku + "/p/?o=" + offer_code
            image_keys=item.get('image_keys')
            product_rating=item.get('product_rating')
            try:
                rating=product_rating.get('value')
                total_rating = product_rating.get('count')
            except:
                rating= None
                total_rating=None

            print("Brand  :",brand)
            print("Product Name: ",name)
            print("Actual Price :", price)
            print("Sale Price :", old_price)
            print("Sku Code :",sku)
            print("Offer Code :",offer_code)
            print("url :",link)

            # for i in image_keys:
            #     image_link = f"https://f.nooncdn.com/p/{i}.jpg?format=avif&width=240"
            #     print("image Link :",image_link)
            print("Product rating value :",rating)
            print("Product rating Count :", total_rating)

            #create dictionary
            insert_data = {
                'brand': brand,
                'product_name': name,
                'price': old_price,
                'old_price': price,
                'link': link,
                # 'image_link': image_link,
                'rating': rating,
                'total_rating': total_rating,
                'date_time': datetime.now()
            }

            key_list = []
            value_list = []
            for key, value in insert_data.items():
                key_list.append('`' + str(key)
 + '`')
                if isinstance(value, str) and '"' in value:
                    value_list.append("'" + value + "'")
                else:
                    value_list.append('"' + str(value) + '"')

            i_key = ','.join(key_list)
            i_value = ','.join(value_list)

            try:
                con = db.cursor()
                query = f"""INSERT INTO db3.beauty_product ({i_key}) VALUES ({i_value})"""
                print(query)
                con.execute(query)
                db.commit()
                print("Data inserted successfully")
            except Exception as e:
                print("Error in insert data: ", e)

        last_page = data.get('nbPages')
        if last_page > page:
            page += 1
            next_url = f"https://www.noon.com/_svc/catalog/api/v3/u/beauty-bestseller-AE/?f%5BisCarousel%5D=true&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc&page={page}"
            print("Page >>> ", page)
            print("Next Page Link :", next_url)
            n.scrap(next_url, page, headers)
        else:
            print("Page Over")

if __name__ == '__main__':
    n = Noon()
    page=1
    url = f'https://www.noon.com/_svc/catalog/api/v3/u/beauty-bestseller-AE/?f%5BisCarousel%5D=true&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc&page={page}'
    headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
    n.scrap(url,page,headers)



















#
# headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
#
# response=requests.get("https://www.noon.com/_next/data/33nfoBY3lWIE0L0GfSQKR/uae-en/beauty-bestseller-AE.json",headers=headers)
#
# a = response.text
# print(a)
# jsondata = json.loads(a)
# print()
#
# P=jsondata ['pageProps']['catalog']['hits']
