import pymysql
# 创建connect对象
connect1 = pymysql.connect(host='localhost', user='root', password='root', db='name_info')
cursor_info = connect1.cursor()  # 获取游标对象
cursor_info.execute("SELECT VERSION()")  # 查询MySQL版本
result = cursor_info.fetchone()  # 获取查询结果
print(result)
cursor_info.close()
connect1.close()  # 关闭数据库连接
