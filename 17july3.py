import json
import requests
import mysql.connector
from datetime import datetime



db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="xbyte"
)

class NoonMobiles:
    def __init__(self):
        c=db.cursor()
        self.table_name='mobile_information'
        self.columns={
            'sr_no': 'INT AUTO_INCREMENT PRIMARY KEY',
            'brand': 'VARCHAR(255)',
            'product_name': 'VARCHAR(255)',
            'price': 'INT',
            'sale_price': 'VARCHAR(255)',
            'link': 'text',
            'image_link': 'VARCHAR(255)',
            'product_rating_value': 'VARCHAR(255)',
            'product_rating_count': 'VARCHAR(255)',
            'date_time': 'varchar(255)',


        }
        column_defination =','.join([f'{col} {self.columns[col]}' for col in self.columns])
        qurey=f'CREATE TABLE IF  NOT EXISTS db3.{self.table_name}({column_defination})'
        c.execute(qurey)
        print("TABLE TO BANA LIYA AB KYA")



    def scrap(self, url, headers):

        response=requests.get(url=url,headers=headers)
        if response.status_code != 200:
            print("Error aavi gayi................")
            return


        try:
            data=response.json()
        except json.JSONDecodeError as e:
            print("eRroR",e)
            return

        hits=data.get('hits')
        if not hits:
            print("error data not found")

            return
        c=db.cursor()
        for item in hits:
            brand=item.get('brand')
            name=item.get('name')
            price=item.get('price')
            sale_price=item.get('sale_price')
            sku=item.get('sku')
            offer_code=item.get('offer_code')
            sku_config=item.get('sku_config')
            image_keys=item.get('image_keys')
            url1=item.get('url')
            link='https://www.noon.com/uae-en/' + url1 + "/" + sku + "/p/?o=" + offer_code

            product_rating=item.get('product_rating')
            product_rating_value=product_rating.get('value') if product_rating else None
            product_rating_count=product_rating.get('count') if product_rating else None

            print("Brand :",brand)
            print("Product Name :", name)
            print("Actual Price:",price)
            print("URL :",link)

            for i in image_keys:
                image_link="https://f.nooncdn.com/p/" + i + ".jpg?format=avif&width=240"
                print("Image Link :", image_link)
            print("Product Rating Value :", product_rating_value)
            print("Product Rating Count :", product_rating_count)
            print("*" * 100)

            insert_data ={
                'brand': brand,
                'product_name': name,
                'price':price,
                'sale_price': sale_price,
                'link':link,
                'image_link':image_link,
                'product_rating_value':product_rating_value,
                'product_rating_count':product_rating_count,
                'date_time':datetime.now()

            }



            keys =[]
            values=[]

            for key,value in insert_data.items():
                keys.append('`'+str(key)+'`')
                if isinstance(value,str) and '"' in value:
                    values.append('`'+value+'`')
                else:
                    values.append('"'+str(value)+'"')

            key_str=','.join(keys)
            value_str=','.join(values)


            try:
                query=f"""INSERT INTO db3.mobile_information ({key_str}) VALUES ({value_str})"""
                c.execute(query)
                db.commit()
                print("data insert sucessfully")
            except Exception as e:
                print("Error in data:",e)

if __name__ == '__main__':
    n=NoonMobiles()
    url=f'https://www.noon.com/_svc/catalog/api/v3/u/huawei/mobiles-top10-brands-23-ae/?f%5BisCarousel%5D=true&sort%5Bby%5D=price&sort%5Bdir%5D=desc'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    n.scrap(url,headers)



















