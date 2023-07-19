import json
import requests
import mysql.connector
from datetime import datetime
import time
import re



db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="xbyte"
)

class Noon:

    def __init__(self):
        c = db.cursor()
        self.table_name = 'sport_product_details'
        self.columns = {
            'sr_no': 'INT AUTO_INCREMENT PRIMARY KEY',
            'brand': 'VARCHAR(255)',
            'product_name': 'VARCHAR(255)',
            'price': 'INT',
            'sale_price': 'VARCHAR(255)',
            'link': 'text',
            'product_rating_value':'VARCHAR(255)',
            'product_rating_count': 'VARCHAR(255)',
            'path':'VARCHAR(255)',
            'description': 'LONGTEXT',
            'specifications': 'LONGTEXT',
            'feature_bullets': 'LONGTEXT',
            'color':'VARCHAR(255)',
            'date_time':'VARCHAR(255)'
        }
        column_definitions = ', '.join([f'{col} {self.columns[col]}' for col in self.columns])
        query = f'CREATE TABLE IF NOT EXISTS db3.{self.table_name} ({column_definitions})'
        c.execute(query)
        print("Table created successfully")

    def scrap(self, link, row):

        path = ''
        product_name = row['product_name']
        brand = row['brand']
        price=row['price']
        sale_price = row['sale_price']

        link = row['link']
        product_rating_value = row['product_rating_value']
        product_rating_count = row['product_rating_count']

        print(link)

        link = str(link).split("en/")[-1]
        url = f'https://www.noon.com/_svc/catalog/api/v3/u/{link}'

        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

        retry_count = 0
        while retry_count < 5:  # Retry up to 5 times
            response = requests.get(url=url, headers=headers)

            try:
                response.raise_for_status()
                data = response.json()
                product_details = data.get('product')

                breadcrumbs = product_details.get('breadcrumbs')
                path = ' > '.join([item.get('name') for item in breadcrumbs])

                description = product_details.get('long_description')
                description = description.replace("'", "") if description is not None else ''

                specs = product_details.get('specifications')
                specifications = " / ".join([f"{i.get('name')}: {i.get('value')}" for i in specs])
                specifications_encoded=specifications.encode('utf-8')
                specifications_cleaned=re.sub(r'[^\x00-\x7F]+', '', specifications)

                color = ""
                groups = product_details.get('groups', [])
                for group in groups:
                    options = group.get('options', [])
                    color += " | ".join([option.get('name') for option in options])

                feature_bullets = " // ".join(product_details.get('feature_bullets', []))

                print("Path :", path)
                print("Long Description : ", description)
                print("Specification : ", specifications)
                print("Colour Options : ", color)
                print("Feature Bullets :", feature_bullets)

                time.sleep(5)  # Delay of 5 seconds between requests

                insert_data = {
                    'brand': brand,
                    'product_name': product_name,
                    'sale_price': sale_price,
                    'price': price,
                    'link': link,
                    'product_rating_value': product_rating_value,
                    'product_rating_count': product_rating_count,
                    'path': path,
                    'description': description,
                    'specifications': specifications,
                    'feature_bullets': feature_bullets,
                    'color': color,
                    'date_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                key_list = []
                value_list = []

                for key, value in insert_data.items():
                    key_list.append('`' + str(key) + '`')
                    if isinstance(value, str) and '"' in value:
                        value_list.append("'" + value + "'")
                    else:
                        value_list.append('"' + str(value) + '"')

                i_key = ','.join(key_list)
                i_value = ','.join(value_list)

                try:
                    con = db.cursor()
                    query = f"""INSERT INTO db3.sport_product_details ({i_key}) VALUES ({i_value})"""
                    print(query)
                    con.execute(query)
                    db.commit()
                    print("Data inserted successfully")
                    try:
                        con = db.cursor()
                        update_query = f'UPDATE db3.sport_information SET status = "completed" WHERE product_name = "{product_name}"'
                        con.execute(update_query)
                        db.commit()
                        print("Status : Completed")
                    except Exception as e:
                        print("Error in status update : ", e)
                    break  # Break out of the retry loop if successful
                except Exception as e:
                    print("Error in insert data: ", e)
                    break  # Break out of the retry loop if unsuccessful

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    retry_count += 1
                    print(f"Too Many Requests. Retrying in 5 seconds... (Retry {retry_count})")

                    time.sleep(2)
                else:
                    print(f"HTTP Error: {e}")
                    break  # Break out of the retry loop if HTTP error occurs

            except json.decoder.JSONDecodeError:
                print("Invalid JSON response")
                break  # Break out of the retry loop if JSON decode error occurs

if __name__ == '__main__':
    n = Noon()
    cursor = db.cursor(dictionary=True)
    sql_select_query = 'SELECT * FROM db3.sport_information where status="pending"'
    cursor.execute(sql_select_query)
    records = cursor.fetchall()

    for row in records:
        link = row['link']
        n.scrap(link, row)
