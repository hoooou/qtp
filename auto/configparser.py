import configparser
 
# ����ConfigParser����
config = configparser.ConfigParser()

#�����ļ�·����
path = "C:/Users/24313/Documents/GitHub/qtp/test/config.ini"

#����ConfigParserģ��
config = configparser.ConfigParser()

#��ȡ�ļ�
config.read(path, encoding="utf-8")

#��ȡ���е�section
sections = config.sections()
print(sections)

# ��ȡ�������ֵ
value = config.get('mailinfo', 'name')

print(value)

# �����������ֵ
config.set('mysqldb', 'sql_host', 'localhost')

# д�뵽�����ļ�
with open(path, 'w') as configfile:
    config.write(configfile)