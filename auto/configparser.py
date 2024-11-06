 
# 创建ConfigParser对象
import configparser
config =configparser.ConfigParser()
#配置文件路径：
path = "/Users/xk/python_project/qtp/auto/config.ini"

#创建ConfigParser模块
config = configparser.ConfigParser()

#读取文件
config.read(path, encoding="utf-8")

#获取所有的section
sections = config.sections()
print(sections)

# 获取配置项的值
value = config.get('mailinfo', 'name')

print(value)

# 更新配置项的值
config.set('mysqldb', 'sql_host', 'localhost')

# 写入到配置文件
with open(path, 'w') as configfile:
    config.write(configfile)