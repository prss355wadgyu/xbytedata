import json
import requests
import mysql.connector
from datetime import datetime
import time

# print("start")

db = mysql.connector.connect(
    host="192.168.1.126",
    user="root",
    password="xbyte"
)

class Noon:

    def __init__(self):
        c = db.cursor()
        self.table_name = 'noon_mobile_details'
        self.columns = {
            'sr_no': 'INT AUTO_INCREMENT PRIMARY KEY',
            'brand': 'VARCHAR(255)',
            'product_name': 'VARCHAR(255)',
            'price': 'INT',
            'sale_price': 'VARCHAR(255)',
            'link': 'text',
            'image_link':'VARCHAR(255)',
            'product_rating_value':'VARCHAR(255)',
            'product_rating_count': 'VARCHAR(255)',
            'path':'VARCHAR(255)',
            'description':'VARCHAR(255)',
            'specifications':'VARCHAR(255)',
            'feature_bullets':'VARCHAR(255)',
            'color':'VARCHAR(255)',
            'date_time':'VARCHAR(255)'
        }
        column_definitions = ', '.join([f'{col} {self.columns[col]}' for col in self.columns])
        query = f'CREATE TABLE IF NOT EXISTS db3.{self.table_name} ({column_definitions})'
        c.execute(query)
        print("Table created successfully")


    def scrap(self,link,row):

        product_name = row['product_name']
        brand=row['brand']
        price = row['price']
        sale_price = row['sale_price']
        image_link = row['image_link']
        product_rating_value = row['product_rating_value']
        product_rating_count=row['product_rating_count']

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        response = requests.get(url=link, headers=headers)
        # data = json.loads(response.text)
        # data = response.json()
        # print(data)
        try:
            response.raise_for_status()
            data = response.json()
            # print(data)

            product_details = data.get('product')

            breadcrumbs = product_details.get('breadcrumbs')
            path = ' > '.join([item.get('name') for item in breadcrumbs])
            try:
                description = product_details.get('long_description').replace("'", "")
            except:
                description = product_details.get('long_description')
            specs = product_details.get('specifications')
            specifications = ""
            for i in specs:
                specifications += i.get('name') + " : " + i.get('value') + " || "

            specification=specifications.replace("'", "")

            color=""
            groups = product_details.get('groups',[])
            for group in groups:
                options = group.get('options', [])
                for option in options:
                    color += option.get('name') + " | "

            feature_bullets = ""
            feature_bullets_list = product_details.get('feature_bullets',[])
            for i in feature_bullets_list:
                feature_bullets += i + " | "

            print("Path :", path)
            print("Long Description : ",description)
            print("specification : ",specification)
            print("Colour Options : ", color)
            print("feature_bullets :", feature_bullets)

        except requests.exceptions.HTTPError as e:
            # print("HTTP Error:", e)
            if response.status_code == 429:
                print(f"Too Many Requests. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"HTTP Error: {e}")

        except json.decoder.JSONDecodeError:
            print("Invalid JSON response")


        time.sleep(5)  # Delay of 5 second between requests

        insert_data = {
            'brand': brand,
            'product_name': product_name,
            'price': price,
            'sale_price': sale_price,
            'link': link,
            'image_link': image_link,
            'product_rating_value': product_rating_value,
            'product_rating_count': product_rating_count,
            'path': path,
            'description': description,
            'specifications': specification,
            'feature_bullets': feature_bullets,
            'color': color,
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
            query = f"""INSERT INTO db3.noon_mobile_details ({i_key}) VALUES ({i_value})"""
            print(query)
            con.execute(query)
            db.commit()
            print("Data inserted successfully")
            try:
                con = db.cursor()
                update_query = f'UPDATE db3.mobile_information  SET status = "completed" WHERE link = "{link}"'
                con.execute(update_query)
                db.commit()
                print("Status : Completed")
            except Exception as e:
                print("Error in status update : ", e)
        except Exception as e:
            print("Error in insert data: ", e)

if __name__ == '__main__':
    n = Noon()
    cursor = db.cursor(dictionary=True)
    sql_select_query = 'SELECT * FROM db3.mobile_information where status="pending"'
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    # print(records)
    for row in records:
        link = row['link']
        n.scrap(link, row)