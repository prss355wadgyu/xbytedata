import mysql.connector
import pymysql
import requests
from scrapy.selector import Selector


db = pymysql.connect(
    host="localhost",
    user="root",
    password="xbyte"
)

class Fddb:
    def __init__(self):
        c = db.cursor()
        self.table_name = 'my_table4'
        self.columns = {
            'sr_no': 'INT AUTO_INCREMENT PRIMARY KEY',
            'page': 'VARCHAR(255)',
            'category': 'VARCHAR(255)',
            'count': 'INT',
            'link': 'VARCHAR(255)',
            'sub_cat':'VARCHAR(255)',
            'sub_item':'VARCHAR(255)',
            'sub_item_link': 'VARCHAR(255)'
        }

        column_definitions = ', '.join([f'{col} {self.columns[col]}' for col in self.columns])
        query = f'CREATE TABLE IF NOT EXISTS db3.{self.table_name} ({column_definitions})'
        c.execute(query)
        print("Table created successfully")


f = Fddb()


def get_data(link, row, page):
    category = row['category']
    count = row['count']
    pre_page = row['page']

    res = requests.get(url=link)
    b = res.text

    response = Selector(text=b)

    for i in response.xpath('//div[@class="standardcontent"]//a[@class="producername"]'):
        sub_cat = i.xpath('.//text()').get()

        for k in i.xpath('./../following-sibling::table//td//a'):
            sub_item = " ".join(k.xpath('.//text()').getall())
            sub_item_link = "https://fddb.info" + ''.join(k.xpath('.//@href').get())

            data = {
                'page': pre_page,
                'category': category,
                'count': count,
                'link': link,
                'sub_cat': sub_cat,
                'sub_item': sub_item,
                'sub_item_link': sub_item_link
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
                query = f"""INSERT INTO my_table4 ({i_key}) VALUES ({i_value})"""
                con.execute(query)
                db.commit()
                print("Data inserted successfully")
            except Exception as e:
                print(e)

    if next:
        page += 1
        link = f"{link.split('/index')[0]}/index{page}.html"
        get_data(link, row, page)


if __name__ == '__main__':
    con = pymysql.connect(host='localhost', user='root', password='xbyte', database='db3')
    crsr = con.cursor(pymysql.cursors.DictCursor)

    sql_select_Query = f'select * from db3.my_table4 where status="pending"'
    crsr.execute(sql_select_Query)
    records = crsr.fetchall()
    for row in records:
        link = row['link']
        page = 0
        get_data(link, row, page)




#############################################################12july

db=pymysql.connect(
    host="localhost",
    user="root",
    password="xbyte",
    database="db3"

)

class Fddb:
    def __init__(self):
        c = db.cursor()
        self.table_name = "my_table7"
        self.columns= {
            'sr_no': 'INT AUTO_INCREMENT PRIMARY KEY',
            'page': 'VARCHAR(255)',
            'category': 'VARCHAR(255)',
            'count': 'INT',
            'link': 'VARCHAR(255)',
            'sub_cat': 'VARCHAR(255)',  # Add the missing column here
            'sub_item': 'VARCHAR(255)',
            'sub_item_link': 'VARCHAR(255)',
            'calorific value':'VARCHAR(255)',
            'calories': 'VARCHAR(255)',
            'protein': 'VARCHAR(255)',
            'carbohydrates': 'VARCHAR(255)',
            'of which sugars': 'VARCHAR(255)',
            'Fat': 'VARCHAR(255)',
            'fiber': 'VARCHAR(255)',
            'bread units': 'VARCHAR(255)',
            'salt': 'VARCHAR(255) default= 0',
            'discription': 'VARCHAR(255)',
            'Manufacturer': 'VARCHAR(255)',
            'Product group': 'VARCHAR(255)'
        }
        column_definitions=', '.join([f'{col} {self.columns[col]}' for col in self.columns])
        query=f'CREATE TABLE IF NOT EXISTS db3.{self.table_name} ({column_definitions})'
        c.execute(query)
        print("Table created successfully")


