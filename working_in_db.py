
import sqlite3

def show_info(message_id):
    conn = sqlite3.connect('faks.db')
    c = conn.cursor()
    c.execute(' SELECT * FROM `users` WHERE message_id = ?' , (message_id,))
    count = c.fetchone()
    count = list(count)
    count.pop(0)
    count.pop(0)
    print(count)
    c.close()
    conn.close()
    return count
def getall():
    conn = sqlite3.connect('faks.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users ''')
    rows = c.fetchall()
    for row in rows:
        print(row)

    c.close()
    conn.close()


def isExist(message_id, text1):
    print(text1)
    text1 = text1.lower()
    print(type(message_id))
    mesid = message_id
    print(type(mesid))
    conn = sqlite3.connect('faks.db')
    c = conn.cursor()
    c.execute(' SELECT * FROM `users` WHERE message_id = ?',(mesid,))
    count = c.fetchone()
    print(count)



    if(count == None):
        c.execute("INSERT INTO `users` values (?,?,?,?)", (None, message_id, None, None))
        conn.commit()
        return 'В базу данных добавлен'

    elif(((text1.find('факультет')>-1) or (text1.find('институт')>-1))  ):
        c.execute('''SELECT * FROM `users` WHERE message_id = message_id ''')
        data = c.fetchone()
        if(data):
            c.execute("UPDATE users SET institut=? WHERE message_id=?", (text1, message_id))
            conn.commit()
        return 'факультет изменен. Не забудь поменять и свою группу'
    elif(((text1.find('бакалавриат')>-1) or (text1.find('магистратура')>-1))  ):
        c.execute('''SELECT * FROM users WHERE message_id = message_id ''')

        data = c.fetchone()
        if(data):
            c.execute("UPDATE users SET fakultet=? WHERE message_id=?", (text1, message_id))
            conn.commit()
            return 'группа изменена. Не забудь проверить, правильное ли у тебя соотношение группы и факультета\института'
    return ''
    c.close()
    conn.close()
def addtable():
    conn = sqlite3.connect('faks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE db
             (fakultet text, groups text, page text)''')
    conn.commit()
    conn.close()
    c.close()

