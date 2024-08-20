#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~ функции работы с БД ~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
import sqlite3

database_name = "/home/clipslemon/neural_network/blurAI.db"

# сделать обработку на ошибку открытия БД
def DB_select_last_name():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Photo ORDER BY id DESC LIMIT 1;')
    select_res = cursor.fetchall()
    if select_res != []:
        last_name = select_res[0][0]
    # список пустой, значит нет записей
    else:
        last_name = 0
    connection.close()
    return last_name

def DB_insert_new_name(last_name):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    
    new_filename = str(last_name + 1) + '.jpg'
    cursor.execute(f"INSERT INTO Photo(processed, way_name) VALUES(0, '{new_filename}')")
    connection.commit()
    connection.close()
    return new_filename

def DB_select_pre_blur():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Photo WHERE Photo.processed = 0 ORDER BY id;")
    name_list = cursor.fetchall()
    for i in name_list:
        print(f'LOG: Photo.processed = 0: {i[0]}')
    connection.close()
    return name_list

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#