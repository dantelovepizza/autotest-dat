import pymysql
from common.op_log import error_log


class Mysql_handler:
    def __init__(self, host, db_name, port, username="root", password="h3croot", charset='utf8'):
        self.db = pymysql.Connect(
            host=host,
            user=username,
            password=password,
            database=db_name,
            port=port,
            charset=charset)
        self.my_cursor = self.db.cursor()
        self.DQL_cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库查询select，返回结果格式为：[{'NAME': '患者主索引'}]
    def DQL_db(self, sql):
        query_result = []
        try:
            self.DQL_cursor.execute(sql)
            query_result = self.DQL_cursor.fetchall()
        except Exception as e:
            error_log.error(e)
        finally:
            self.DQL_cursor.close()
        return query_result

    # 数据操作语句 insert、delete、update
    def DML_db(self, sql):
        try:
            self.my_cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            error_log.error(e)
            self.db.rollback()
        finally:
            self.my_cursor.close()

    def connect_close(self):
        self.db.close()


if __name__ == '__main__':
    pass
    # SQL = r"SELECT * from sys_user_type "
    # # insert = r"insert into sys_user_type (id,name) values('123','nan')"
    # delete = r"delete from   sys_user_type where  id ='123'"
    # db = Mysql_handler('192.168.11.119', 'hxyy-portal', 13306)
    # result = db.DQL_db(SQL)
    # db.DML_db(delete)
    # print(len(result))


