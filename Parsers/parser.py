from flask import Flask, render_template, request, redirect, send_file
from hh_parser import get_hh_jobs
from export_parser import save_to_csv

app = Flask(__name__)

# Создание пустого БД (для быстрого поиска вакансии | оптимизация поиска)
db = {}

@app.route('/')
def home():
    return render_template('home.html')

# Поиск
@app.route('/report')
def report():
    # Поиск по ключевому слову
    keyword = request.args.get('keyword')
    # Если ключевое слово есть в запросе, 
    if keyword is not None:
        # тогда мы выводим запрос в нижнем регистре (для эстетики)
        keyword = keyword.lower()
        # Создание записи или открытие записей БД
        # ** поиск в БД записи ранее вводимого словаря **
        getDb = db.get(keyword)
        # Если запись существует, то мы выводим ее сразу
        if getDb:
            jobs = getDb
        # Если в БД нет записи данного поискового слова, то мы добавляем его в наш словаь db
        else:
            # Запускаем парсер 'get_hh_jobs' с ключеввым словом 'keyword'
            jobs = get_hh_jobs(keyword)
            # Записываем полученный результат в нашу db
            db[keyword] = jobs
    else:
        # Возврат на главную страницу, если пользователь перешел по ссылки поиска вакансии, 
        # но не ввел ключевое слово
        return redirect('/')
    # searchBy - имя для шаблона, resultNumber - количество найденных вакансий
    return render_template('report.html', searchBy=keyword, resultNumber=len(jobs), jobs=jobs)             
    # jobs=jobs - получение всех записей

@app.route('/export')
def export():
    # Если переход по URL валиден
    try:
        keyword = request.args.get('keyword')
        # Если пользователь не вел ключевое слово, но перешел по ссылке для скачивания парсера 
        # в CSV формате, то мы вызываем ошибку и возвращаем пользователя на главную страницу
        if not keyword:                
            raise Exception()          
        keyword = keyword.lower()
        jobs = db.get(keyword)
        # Если в БД нет ключевого слова по данной вакансии, то мы вызываем ошибку
        if not jobs:
            raise Exception()
        # Возвращаем запрос на файл
        # Сохраняем парсер в CSV файл
        save_to_csv(jobs)
        return send_file('jobs.csv')
    # Если переход по URL не валидный, то мы переходим на главную страницу
    except:
        return redirect('/')

# Динамические URL -  адресса
# @app.route('/<username>')                       # <> - плейсхолдер
# def username_title(username):                   # Если мы передаем параметр в плейсхолдере, то мы должны
#     return f'Hello, {username}!'                # его принимать в функции, иначе будет выведена ошибка!

app.run(host="127.0.0.1")