import pprint
import pymysql

# 创建connect对象插入中文需要指定编码
connect = pymysql.connect(host='localhost', user='root', password='root', db='name_info', charset='utf8')
# 获取游标对象查询返回字典
cursor = connect.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM users")
result = cursor.fetchall()
print("更新前")
pprint.pprint(result)
cursor.execute("UPDATE users SET name='高手' WHERE id = 2")  # 更新name字段
connect.commit()
cursor.execute("SELECT * FROM users")
result = cursor.fetchall()
print("更新后")
pprint.pprint(result)
cursor.close()
connect.close()