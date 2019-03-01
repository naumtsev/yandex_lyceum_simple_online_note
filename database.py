import sqlite3
import os.path
import time

class DB:
    def __init__(self):
        conn = sqlite3.connect('news.db', check_same_thread=False)
        self.connection = conn

    def get_connection(self):
        return self.connection

    def __del__(self):
        self.connection.close()



class NewsModel:
    def __init__(self, data_base):
        self.connection = data_base.get_connection()
        self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             title VARCHAR(128),
                             content VARCHAR(1200),
                             date INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, title, content):
        cursor = self.connection.cursor()
        date = time.time()
        cursor.execute('''INSERT INTO news 
                          (user_name, title, content, date) 
                          VALUES (?,?,?,?)''', (user_name, title, content, str(date)))
        cursor.close()
        self.connection.commit()

    def get(self, post_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(post_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_name=None):
        cursor = self.connection.cursor()
        if user_name != None:
            cursor.execute('SELECT * FROM news WHERE user_name = "{}"'.format(user_name))
        else:
            cursor.execute("SELECT * FROM news")

        rows = cursor.fetchall()
        return rows

    def delete(self, post_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM news WHERE id = ?', (str(post_id)))
        cursor.close()
        self.connection.commit()

    def clear(self):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM news')
        cursor.close()
        self.connection.commit()

    def __str__(self):
        return str(self.get_all())

    def sort_by_date(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM news ORDER BY date')
        cursor.close()
        self.connection.commit()

    def sort_by_alph(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM news ORDER BY title')
        cursor.close()
        self.connection.commit()

class UserModel:
    def __init__(self, data_base):
        self.connection = data_base.get_connection()
        self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash) 
                          VALUES (?,?)''', (user_name, password_hash))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", str(user_id))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()

        if row:
            return (True, row[0])
        return (False, )

    def user_name_is_free(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_name = "{}"'.format(user_name))
        row = cursor.fetchone()
        if row:
            return False
        return True

    def delete(self, id_user):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(id_user)))
        cursor.close()
        self.connection.commit()

    def clear(self):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM users')
        cursor.close()
        self.connection.commit()

    def __str__(self):
        return str(self.get_all())

    def count_by_username(self, username):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(user_name) FROM news WHERE user_name = "{}"'.format(username))
        row = cursor.fetchone()
        if not row:
            return 0
        return row[0]


my_db = DB()
users = UserModel(my_db)
news = NewsModel(my_db)
print(users.count_by_username('123'))