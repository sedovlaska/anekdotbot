import sqlite3
from sqlite3 import Error

class SQLighter:
    def __init__(self,database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, user_name):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute('INSERT INTO `subs` (`user_id`, `user_name`) VALUES(?,?)', (user_id,user_name))

    def user_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `subs` WHERE `user_id`=?",(user_id,)).fetchall()
            return bool(len(result))

    def save_text(self,text,user_name):
        with self.connection:
            return self.cursor.execute('INSERT INTO `anekdot` (`text`,`user_name`) VALUES(?,?)',(text,user_name))

    def check_text(self,text):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `anekdot` WHERE `text` = ?',(text,)).fetchall()
            return bool(len(result))

            
    def close(self):
        self.connection.close()

