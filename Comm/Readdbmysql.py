
from ApiTest.Comm.Logtype import loggings
import pymysql


class DBmysql:

    def __init__(self, host, port, username, pswd, dbname):
        loggings.info('连接数据库'+dbname)
        self.conn = pymysql.connect(
            host=host,
            user=username,
            port=int(port),
            password=pswd,
            db=dbname,
            charset='utf8',
            # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
        )
        # ****python, 必须有一个游标对象， 用来给数据库发送sql语句， 并执行的.
        # 2. 创建游标对象，
        self.cur = self.conn.cursor()

    # def creat_table(self, create_sql):
    #     try:
    #         loggings.info('执行创建新表' + create_sql)
    #         self.cur.execute(create_sql)
    #
    #     except Exception as e:
    #         print("创建数据表失败:", e)
    #     else:
    #         print("创建数据表成功;")

    # def insert_sql(self, sql):
    #
    #     excel = ReadExcel('Data', 'tihuo.xlsx', 'Sheet1')
    #     List = excel.read_data(1, None)
    #
    #     loggings.info('执行插入数据'+sql)
    #     self.cur.executemany(sql, List)
    #
    #     self.conn.commit()   # 如果是插入数据， 一定要提交数据， 不然数据库中找不到要插入的数据;
    #     print("插入数据成功;")
    #     List.clear()
    #     self.conn.close()
# import astext
    def select_sql(self, sql):
        try:
            loggings.info('执行查询语句：' + sql)
            self.cur.execute(sql)

            result = self.cur.fetchall()
            lis = self.cur.description
            # print(lis)
            lt = []
            for i in lis:
                lt.append(i[0])

            # loggings.info('查询结果为'+str(result))
            print('列名-->>' + str(lt))
            print('查询数据-->>' + str(result))
            return result                 # 返回一个元组对象

        except Exception as e:
            print('没有找到数据:', e)
        self.conn.close()

    def delete_sql(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            loggings.info('执行删除语句成功：' + sql)
        except Exception as e:
            print('数据删除失败', e)
            loggings.error('数据删除失败,回滚数据')
            self.conn.rollback()
        self.conn.close()


if __name__ == '__main__':
    sqls = DBmysql('101.132.243.1', 3306, 'center', 'center6200', 'centerdb_test1')
#     sqls.insert_sql('INSERT INTO test1 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
#     %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);')
    sqls.select_sql('select title from t_banner where id=53')
#     sqls.delete_sql('sql')
