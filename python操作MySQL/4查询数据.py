import pprint
import pymysql

# 创建connect对象插入中文需要指定编码
connect = pymysql.connect(host='localhost', user='root', password='root', db='name_info', charset='utf8')
# 获取游标对象查询返回字典
cursor = connect.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM user")
# 只返回一个
result = cursor.fetchone()
print("返回一条记录")
pprint.pprint(result)
cursor.execute("SELECT * FROM user")
# 全部返回
result = cursor.fetchall()
print("返回全部记录")
pprint.pprint(result)
cursor.close()
connect.close()
