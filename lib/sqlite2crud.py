import os
import random
import sqlite3
import string


class sqlite2CRUD:
    db_name='example.db'

    def __init__(self, db_name=None):
        if db_name is not None:
            self.db_name = db_name
        else:
            self.db = self.db_name
        self.conn = self.connect(self.db_name)
        self.cursor = self.conn.cursor()
        if self.cursor:
            print('Database is connected.')
        else:
            print('Database is not connected.')


    def connect(self, db_name):
        if not os.path.exists(db_name):
            print('System will create a new database, named '+db_name+' .')
        connect = sqlite3.connect(db_name)
        return connect

    def _create(self, sql):
        self.__common__(sql)

    def _read(self, sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def _update(self, sql):
        self.__common__(sql)

    def _delete(self, sql):
        self.__common__(sql)

    def __common__(self, sql):
        self.cursor.execute(sql)
        try:
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def close(self):
        print('It\'s disconnected.')
        self.conn.close()

def main():
    c = sqlite2CRUD()

    if c._read('select count(1) from sqlite_master where name=\'LPR\'')[0][0] <= 0:
        sql = '''
        create table LPR(
            id integer primary key autoincrement not null,
            name text unique not null,
            des nchar(255) null,
            predict nchar(16) null,
            color nchar(10) null,
            accurate tinyint null default(null),
            datetime not null default(datetime('now', 'localtime'))
        )

        '''
        c._create(sql)
    else:
        if c._read('select count(1) from LPR')[0][0]<= 0:
            size = 100
            for _ in range(size):
                pic_format = '.'+''.join(random.choice(['jpg','png']))
                filename = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                new_filename = filename+pic_format
                des = random.choice(['opencv+ocr','opencv+svm','opencv+cnn','yolo+cnn'])
                predict = (''.join(random.sample(string.ascii_letters, 2)) +'-'+ ''.join(random.sample(string.digits, 4))).upper()
                color = random.choice(['white','black','red','green','blue','yellow'])
                # print(new_filename, des, predict, color)
                sql = '''
                insert into LPR(name, des, predict ,color)
                select \'%s\',\'%s\',\'%s\',\'%s\'
                '''%(new_filename,des,predict,color)
                # print(sql)
                c._create(sql)

        c._read('select * from LPR limit 1')
        col_name= [i[0] for i in c.cursor.description]
        print(col_name)

        for row in c._read('select * from LPR'):
            print('row:', row)

    c.close()

if __name__ == '__main__':
    # main()
    pass
