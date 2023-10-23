import pprint
import pymysql

create_sql = """
CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `age` INT NULL,
  PRIMARY KEY (`id`))
DEFAULT CHARACTER SET = utf8;
"""
# 创建connect对象
connect1 = pymysql.connect(host='localhost', user='root', password='root', db='name_info')
cursor = connect1.cursor()  # 获取游标对象
# cursor.execute(create_sql)  # 创建数据表
cursor.execute("DESC users")    # 查询创建的新表结构
result = cursor.fetchall()
pprint.pprint(result)
cursor.close()
connect1.close()