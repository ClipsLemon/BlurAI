import os, sys
sys.path.append(os.path.join(os.getcwd(), '..'))

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import db_func
# from content.ai.src import find_blur
from content.ai.src import find_blur



# Инициализация приложения flask
app = Flask(__name__)

# Папки для хранения загруженных фото
upload_folder = "/home/clipslemon/neural_network/in_predictions/"
photos_folder = "/home/clipslemon/neural_network/out_predictions/"
# Проверка наличия этой самой папки
if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

# Настройка
app.config['UPLOAD_FOLDER'] = upload_folder

# Допустимые расширения
allowed_extensions = ['jpg', 'png', 'jpeg']

# Проверка на допустимые расширения
def check_file_extension(filename):
    return filename.split('.')[-1] in allowed_extensions


# Рендер html страницы
@app.route('/')
def site():
    return render_template('index.html')

# загрузка файла
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':  # Проверка на метод
        files = request.files.getlist('files')  # Получение фото
        name_list = []
        for f in files:
            # Сохранение фото в папке upload
            if check_file_extension(f.filename):
                # last_name int, id фотки
                last_name = db_func.DB_select_last_name()
                # получаем новое название из последнего старого
                f.filename = db_func.DB_insert_new_name(last_name)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))  # secure_filename проверяет безопасность файла
                #формируем списокимен загруженных файлов, чтобы передать в нейронку
                name_list.append(upload_folder+f.filename)
        find_blur.blur_objects(name_list)
        # DB_select_pre_blur()
        return index()
    return render_template('index.html')


#импорт файлов нейронки
#from ai.src import *
#from ai import *
#функция обработки фото нейронки



#выгрузка фото из второй папки
@app.route('/photos', methods=['POST'])
def index():
    # Получаем список файлов в папке с фотографиями
    # когда будет налажена работа с нейронкой, здесь upload_folder меняется на photos_folder, туда нейронка выгрузит резы
    photos = sorted(os.listdir(photos_folder), key=lambda x: os.path.getctime(os.path.join(photos_folder, x)))

    # Вытаскиваем последнюю загруженную фотографию
    last_photo = photos[-1]

    # Отдаем фотографию на сайт
    return render_template('index.html', photo=last_photo)


@app.route('/photos/<path:filename>')
def photo(filename):
    # Отправляем запрошенную фотографию
    # когда будет налажена работа с нейронкой, здесь upload_folder меняется на photos_folder, туда нейронка выгрузит резы
    return send_from_directory(photos_folder, filename)



if __name__ == '__main__':
    app.run()  # Запуск приложения