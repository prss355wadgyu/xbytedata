import mysql.connector
import requests
from scrapy.selector import Selector

db = mysql.connector.connect(
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
            'link': 'VARCHAR(255)'
        }

        column_definitions = ', '.join([f'{col} {self.columns[col]}' for col in self.columns])
        query = f'CREATE TABLE IF NOT EXISTS db3.{self.table_name} ({column_definitions})'
        c.execute(query)
        print("Table created successfully")

f=Fddb()

for i in range(97, 123):
    # print(chr(i))
    url = requests.get(f"https://fddb.info/db/de/hersteller/{chr(i)}.html")
    urls=f'//div[@class="standardcontent"]//p[@style="" or @style="padding-left:6px;"]//a'
    response = Selector(text=url.text)
    c = response.xpath('//div[@class="standardcontent"]//p[@style="" or @style="padding-left:6px;"]//a')
    for j in c:
        page = chr(i)
        print(page)



        category = j.xpath('''.//text()''').get()
        # print(category)

        count = j.xpath('''./following-sibling::span[@class="numberofitems"]//text()''').get().strip('()')
        # print(count)

        links = j.xpath('''.//@href''').getall()
        link="https://fddb.info/" + ''.join(links)
        # print(link)



        data = {
            'page': chr(i),
            'category': category,
            'count': count,
            'link': link#.replace('"', '\"')
        }

        key_list = []
        value_list = []
        for key, value in data.items():
            key_list.append('`'+str(key)+'`')
            if '"' in value:
                value_list.append("'"+value+"'")
            else:
                value_list.append('"'+value+'"')

        i_key = ','.join(key_list)
        i_value = ','.join(value_list)

        try:
            con = db.cursor()
            query = f"""INSERT INTO db3.my_table4 ({i_key}) VALUES ({i_value})"""
            con.execute(query)
            db.commit()
            print("Data inserted successfully")
        except Exception as e:
            print(e)

    query=f"UPDATE my_table4 SET status = 'completed' WHERE url=urls"