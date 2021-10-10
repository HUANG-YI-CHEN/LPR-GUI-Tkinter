import logging
import os
import random
import sqlite3
import string


class Sqlite2CRUD:
    db_name='example.db'

    def __init__(self, db_name=None):
        if db_name:
            self.db_name = db_name
        else:
            self.db_name = self.db_name
        self.conn = self.connect(self.db_name)
        self.cursor = self.cursor(self.conn)
        if self.cursor:
            logging.info(':Database is connected.')
        else:
            logging.info(':Database is not connected.')

    def set_database(self, db_name):
        self.db_name = db_name

    def connect(self, db_name):
        if not os.path.exists(db_name):
            logging.info('System will create a new database, named '+db_name+' .')
        connect = None
        try:
            connect = sqlite3.connect(db_name)
        except:
            logging.info('Catch an exception.', exc_info=True)
        return connect

    def cursor(self, connect):
        cursor = None
        if connect:
            cursor = connect.cursor()
        return cursor

    def _create(self, sql):
        self.__common(sql)

    def _insert(self, sql):
        self.cursor.execute(sql)
        row_id = None
        try:
            self.conn.commit()
            row_id = self.cursor.lastrowid
        except:
            self.conn.rollback()
            logging.info('Catch an exception.', exc_info=True)
        return row_id

    def _read(self, sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def _update(self, sql):
        self.__common(sql)

    def _delete(self, sql):
        self.__common(sql)

    def __common(self, sql):
        self.cursor.execute(sql)
        try:
            self.conn.commit()
        except:
            self.conn.rollback()
            logging.info('Catch an exception.', exc_info=True)

    def close(self):
        logging.info('It\'s disconnected.')
        self.conn.close()

class LPR_SQL:
    def __init__(self, conn:Sqlite2CRUD):
        self.conn = conn

    def init_db(self):
        logging.info('=' * 40)
        if self.conn._read('select count(1) from sqlite_master where name=\'Type\'')[0][0] <= 0:
            sql = '''
            create table Type (
                tid integer primary key autoincrement not null,
                extend nchar(50) not null,
                type nchar(15) not null,
                subtype ncahr(255) null,
                unique(extend, type) on conflict replace
            )
            '''
            self.conn._create(sql)
            logging.info('Type table is established.')

        if self.conn._read('select count(1) from sqlite_master where name=\'File\'')[0][0] <= 0:
            sql = '''
            create table File (
                fid integer primary key autoincrement not null,
                folder text not null,
                fname text not null,
                type tinyint not null,
                des text null,
                since not null default(datetime('now', 'localtime')),
                lastmodified not null default(datetime('now', 'localtime')),
                foreign key (type) references Type(tid),
                unique(folder, fname, type) on conflict replace
            )
            '''
            self.conn._create(sql)
            logging.info('File table is established.')

        if self.conn._read('select count(1) from sqlite_master where name=\'LPR\'')[0][0] <= 0:
            sql = '''
            create table LPR (
                lid integer primary key autoincrement not null,
                method nchar(255) null,
                plate nchar(16) null,
                color nchar(10) null,
                predict tinyint null,
                revise nchar(16) null,
                accuracy float null,
                since not null default(datetime('now', 'localtime'))
            )
            '''
            self.conn._create(sql)
            logging.info('LPR table is established.')

        if self.conn._read('select count(1) from sqlite_master where name=\'FLRel\'')[0][0] <= 0:
            sql = '''
            create table FLRel (
                fid int integer not null,
                lid int integer not null,
                des nchar(255) null,
                foreign key (fid) references File(fid),
                foreign key (lid) references LPR(lid),
                primary key(fid, lid)
            )
            '''
            self.conn._create(sql)
            logging.info('FLRel table is established.')

        if self.conn._read('select count(1) from sqlite_master where name=\'vd_info\'')[0][0] <= 0:
            sql = '''
                create view vd_info as
                select l.lid, f.folder, f.fname|| '' ||t.extend as filename,
                    t.type as format, l.method, l.plate, l.color, l.predict, l.revise, l.since
                from File as f, Type as t, FLRel as rel ,LPR as l
                where f.type = t.tid and f.fid = rel.fid and rel.lid = l.lid
            '''
            self.conn._create(sql)
            logging.info('vd_info view is established.')

        if self.conn._read('select count(1) from Type')[0][0] <= 0:
            sql = '''
            insert into Type (extend, type, subtype) values
                ('.bmp','image','bmp'),('.gif','image','gif'),('.ico','image','vnd.microsoft.icon'),('.jpg','image','jpeg'),('.jpeg','image','jpeg'),
                ('.png','image','png'),('.svg','image','svg+xml'),('.tif','image','tiff'),('.tiff','image','tiff'),('.webp','image','webp'),
                ('.avi','video','x-msvideo'),('.flv','video','x-flv'),('.mov','video','quicktime'),('.mp4','video','mp4'),('.mpeg','video','mpeg'),
                ('.ogv','video','ogg'),('.ts','video','mp2t'),('.webm','video','webm'),('.wmv','video','x-ms-wmv'),('.3gp','video','3gpp')
            '''
            self.conn._create(sql)
            logging.info('Type table rows insert OK.')
        logging.info('=' * 40)

    def delete_tb(self, tb_name:str):
        sql = 'select count(1) from sqlite_master where name=\'%s\'' % (tb_name)
        if self.conn._read(sql)[0][0] > 0:
            sql = 'drop table %s'%(tb_name)
            self.conn._create(sql)
            logging.info('drop table %s'%(tb_name))

    def delete_vd(self, vd_name:str):
        sql = 'select count(1) from sqlite_master where name=\'%s\'' % (vd_name)
        if self.conn._read(sql)[0][0] > 0:
            sql = 'drop view %s'%(vd_name)
            self.conn._create(sql)
            logging.info('drop view %s'%(vd_name))

    def delete_all(self):
        logging.info('=' * 40)
        tb_names = ['vd_info', 'FLRel', 'LPR', 'File', 'Type']
        for tb in tb_names:
            try:
                self.delete_tb(tb)
            except:
                self.delete_vd(tb)
        logging.info('delete all table finished')
        logging.info('=' * 40)

    def insert_File(self, file_path, des=''):
        folder = os.path.dirname(file_path)
        fname = (os.path.basename(file_path)).split('.')[0]
        fmt = os.path.splitext(file_path)[1]

        sql = 'select tid from Type where extend=\'%s\''%(fmt)
        tid = self.conn._read(sql)[0][0]

        row_id = None
        sql = 'select count(1) from File where folder=\'%s\' and fname=\'%s\' and type=%d'%(folder, fname, tid)
        if self.conn._read(sql)[0][0] <= 0:
            sql = 'insert into File(folder, fname, type, des) values(\'%s\',\'%s\',%d, \'%s\')'%(folder, fname, tid, des)
            row_id = self.conn._insert(sql)
        else:
            sql = 'select fid from File where folder=\'%s\' and fname=\'%s\'and type=%d'%(folder, fname, tid)
            row_id = self.conn._read(sql)[0][0]
            sql = 'update File set lastmodified=datetime(\'now\', \'localtime\') where fid = %d'%(row_id)
            self.conn._update(sql)
        return row_id

    def update_File(self, fid: int, des=''):
        sql = 'select fid from File where fid=%d'%(fid)
        if self.conn._read(sql)[0][0]:
            sql = 'update File set des = \'%s\', lastmodified = datetime(\'now\', \'localtime\') where fid = %d' % (des, fid)
            row_id = self.conn._update(sql)

    def insert_LPR(self, method, plate, color, predict=None, revise=None):
        sql = '''
            insert into LPR(method, plate, color, predict, revise) values (\'%s\',\'%s\',\'%s\',%s, %s)
        ''' % (method, plate, color, 'null' if predict is None else str(predict), 'null' if revise is None else '\''+revise+'\'')
        row_id =  self.conn._insert(sql)
        return row_id

    def update_LPR(self, row_id:int, predict=None, revise=None):
        sql = '''
            update LPR set predict = %s, revise = %s where lid = %d
        ''' % ('null' if predict is None else str(predict), 'null' if revise is None else '\''+revise+'\'', row_id)
        self.conn._update(sql)

    def insert_FLRel(self, fid:int, lid:int):
        sql = 'select count(1) from FLRel where fid=%d and lid=%d'%(fid, lid)
        if self.conn._read(sql)[0][0] <= 0:
            sql = 'insert into FLRel(fid, lid) values(%d, %d)' % (fid, lid)
            self.conn._insert(sql)

    def random_test(self, size=10):
        for _ in range(size):
            folder = os.path.abspath(os.curdir)
            pic_format = '.'+''.join(random.choice(['jpg','png']))
            filename = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            new_filename = os.path.abspath( os.path.join(folder, filename+pic_format) )
            method = random.choice(['opencv+ocr','opencv+svm','opencv+cnn','yolo+cnn'])
            plate = (''.join(random.sample(string.ascii_letters, 2)) +'-'+ ''.join(random.sample(string.digits, 4))).upper()
            color = random.choice(['white','black','red','green','blue','yellow'])

            # logging.info(new_filename, method, plate, color)
            row_fid = self.insert_File(new_filename)
            row_lid = self.insert_LPR(method, plate, color, predict=None, revise=None)
            self.insert_FLRel(row_fid, row_lid)


def main():
    db_path = os.path.join(os.path.abspath(os.path.curdir),'source','example.db')
    conn = Sqlite2CRUD(db_path)
    lpr = LPR_SQL(conn)
    lpr.delete_all()
    lpr.init_db()
    lpr.random_test(100)

    conn._read('select * from vd_info limit 1')
    col_name= [i[0] for i in conn.cursor.description]
    logging.info(col_name)

    for row in conn._read('select * from vd_info'):
        logging.info('row:', row)

    conn.close()

if __name__ == '__main__':
    # main()
    pass
