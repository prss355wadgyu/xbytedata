import mysql.connector
import pymysql
import requests
from scrapy.selector import Selector
import re

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="xbyte"
)

class Fddb:
    def __init__(self):
        c = db.cursor()
        self.table_name = 'sub_cat_table1'
        self.columns = {
            'sr_no': 'INT AUTO_INCREMENT PRIMARY KEY',
            'page': 'VARCHAR(255)',
            'category': 'VARCHAR(255)',
            'count': 'INT',
            'link': 'VARCHAR(255)',
            'sub_cat':'VARCHAR(255)',
            'sub_item':'VARCHAR(255)',
            'sub_item_link': 'VARCHAR(255)',
            'path': 'VARCHAR(255)',
            'manufacturer': 'VARCHAR(255)',
            'description': 'VARCHAR(255)',
            'sub_cat_item': 'VARCHAR(255)',
            'sub_cat_item_value': 'VARCHAR(255)'
        }
        column_definitions = ', '.join([f'{col} {self.columns[col]}' for col in self.columns])
        query = f'CREATE TABLE IF NOT EXISTS db3.{self.table_name} ({column_definitions})'
        c.execute(query)
        print("Table created successfully")



def get_data(sub_item_link,row):
    pre_page = row['page']
    category = row['category']
    count = row['count']
    link=row['link']
    sub_cat=row['sub_cat']
    sub_item=row['sub_item']


    res = requests.get(url=sub_item_link)

    # output = res.text
    #
    # with open(f'D:\Sagar\Html content\{sub_cat}.html', 'w', encoding='utf-8') as f:
    #     f.write(output)

    response = Selector(text=res.text)

    path1=''.join(response.xpath('//div[@class="breadcrumb"]//text()').getall())
    path = re.sub(' +', ' ',path1)

    description=response.xpath('//p[@class="lidesc2012"]//text()').get()

    manufacturer=category

    for i in response.xpath('//div[@class="standardcontent"]//div[@class="sidrow"]'):
        sub_cat_item= i.xpath('.//text()').get()
        sub_cat_item_value=i.xpath('.//following-sibling::div//text()').get()

        print("Sub category items : ", sub_cat_item)
        print("Values :", sub_cat_item_value)

        # print("Path :",path)
        # print("Category :", category)
        # print("Sub Item :", sub_item)

        # print('Description : ',description)
        # print(manufacturer)
        # print("\n"*"*"*50)

        data = {
            'page': pre_page,
            'category': category,
            'count': count,
            'link': link,
            'sub_cat': sub_cat,
            'sub_item': sub_item,
            'sub_item_link': sub_item_link,
            'path':path,
            'manufacturer':manufacturer,
            'description':description,
            'sub_cat_item':sub_cat_item,
            'sub_cat_item_value':sub_cat_item_value
        }

        key_list = []
        value_list = []
        for key, value in data.items():
            key_list.append('`' + str(key)+ '`')
            if isinstance(value, str) and '"' in value:
                value_list.append("'" + value + "'")
            else:
                value_list.append('"' + str(value) + '"')

        i_key = ','.join(key_list)
        i_value = ','.join(value_list)

        try:
            con = db.cursor()
            query = f"""INSERT INTO db3.sub_cat_table1 ({i_key}) VALUES ({i_value})"""
            con.execute(query)
            db.commit()
            print("Data inserted successfully")
            try:
                con = db.cursor()
                update_query = f'UPDATE db3.my_table4 SET status = "completed" WHERE sub_item = "{sub_item}"'
                con.execute(update_query)
                db.commit()
                print("Status : Completed")
            except Exception as e:
                print("Error : ", e)
        except Exception as e:
            print("Error : ",e)


if __name__ == '__main__':
    f=Fddb()
    cursor = db.cursor(dictionary=True)
    sql_select_query = 'SELECT * FROM db3.my_table4 where status="pending"'
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    print(records)
    # for row in records:
    #     sub_item_link = row['sub_item_link']
    #     get_data(sub_item_link, row)