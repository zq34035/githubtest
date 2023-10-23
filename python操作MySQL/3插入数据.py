import pprint
import pymysql

insert_sql = """
INSERT INTO users (id, name, age)
 VALUES (1, 'Python新手', 20),(2, 'Python高手', 40)
"""

# 创建connect对象
connect1 = pymysql.connect(host='localhost', user='root', password='root', db='name_info')
cursor = connect1.cursor()  # 获取游标对象
try:
    cursor.execute(insert_sql)  # 插入数据
    connect1.commit()
except Exception as e:
    connect1.rollback()  # 发生错误回滚
cursor.close()
connect1.close()
