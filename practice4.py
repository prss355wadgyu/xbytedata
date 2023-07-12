import mysql.connector
import pymysql
import requests
from scrapy.selector import Selector


db = pymysql.connect(
    host="localhost",
    user="root",
    password="xbyte",
    database="db3"
)

class Fddb:
    def __init__(self):
        c = db.cursor()
        self.table_name = 'data1'
        self.columns = {
            'sr_no': 'INT AUTO_INCREMENT PRIMARY KEY',
            'page': 'VARCHAR(255)',
            'category': 'VARCHAR(255)',
            'count': 'INT',
            'link': 'VARCHAR(255)',
            'sub_cat': 'VARCHAR(255)',  # Add the missing column here
            'sub_item': 'VARCHAR(255)',
            'sub_item_link': 'VARCHAR(255)'
        }

        column_definitions = ', '.join([f'{col} {self.columns[col]}' for col in self.columns])
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({column_definitions})'
        c.execute(query)
        db.commit()
        print("Table created successfully")


def get_data(link, row, page):
    category = row['category']
    count = row['count']

    pre_page = row['page']

    res = requests.get(url=link)
    b = res.text

    response = Selector(text=b)

    for i in response.xpath('//div[@class="standardcontent"]//a[@class="producername"]'):
        sub_cat = i.xpath('.//text()').get()
        print(category)
        print(sub_cat)

        for k in i.xpath('./../following-sibling::table//td//a'):
            sub_item = " ".join(k.xpath('.//text()').getall())
            sub_item_link = "https://fddb.info" + ''.join(k.xpath('.//@href').get())
            print(sub_item)
            print(sub_item_link)

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
                key_list.append('`' + str(key) + '`')
                if isinstance(value, str) and '"' in value:
                    value_list.append("'" + value + "'")
                else:
                    value_list.append('"' + str(value) + '"')

            i_key = ','.join(key_list)
            i_value = ','.join(value_list)

            try:
                con = db.cursor()
                query = f"""INSERT INTO data1 ({i_key}) VALUES ({i_value})"""
                con.execute(query)
                db.commit()
                print("Data inserted successfully")
            except Exception as e:
                print(e)



    try:
        con=db.cursor()
        query=f"""update my_table4 set status='Done' where category='{category}'"""
        con.execute(query)
        db.commit()
        print("Record Updated......")

    except Exception as e:
        print(e)









    if response.xpath('//div[@class="leftblock"]//table//td//span//a/@href'):
        page+=1
        link=f"{link.split('/index')[0]}/index{page}.html"
        get_data(link, row, page)
        print(f"Page : ", {page})


if __name__ == '__main__':
    f = Fddb()  # Move the creation of Fddb object here

    con = pymysql.connect(host='localhost', user='root', password='xbyte', database='db3')
    crsr = con.cursor(pymysql.cursors.DictCursor)

    sql_select_Query = f'select * from my_table4 where status="Pending"'
    crsr.execute(sql_select_Query)
    records = crsr.fetchall()
    for row in records:
        link = row['link']
        page = 0
        get_data(link, row, page)
