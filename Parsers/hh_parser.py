import requests
from bs4 import BeautifulSoup

# Инициализируем вход на сайт с помощью небольшой манипуляции 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

def extract_max_pages(url):
    
    hh_request = requests.get(url, headers=headers)
    hh_soup = BeautifulSoup(hh_request.text, 'html.parser')     # Выводим текст в консоль с помощью text | 'html.parser' - обязательный параметр

    pages = []                                                  # Создаем пустой список для нашего цикла page

    paginator = hh_soup.find_all("span", {'class': 'pager-item-not-in-short-range'})   # Вытаскиваем 'div' с классом 'pager...'

    for page in paginator:                                      # Проходимся по циклу от нашего запроса
        pages.append(int(page.find('a').text))                  # Добавляем все элементы с классом 'a' в созданный список pages

    return pages[-1]

def extract_job(html):
    title = html.find('a').text                                 # Вытаскиваем название вакансий
    link = html.find('a')['href'] 
    company = html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a')
    if company is not None:
        company = company.text.strip().replace("\xa0", ' ')
    else:
        company = 'None'
    location = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location = location.split(',')[0]
    return {'title': title, 'company': company, 'location': location, 'link': link}

def extract_jobs(last_page, url):                                 # last_page - номер последней страницы
    jobs = []
    for page in range(last_page):
        print(f'Парсинг страницы {page}')
        result = requests.get(f'{url}&page={page}', headers=headers)     # Получаем ссылки на все страницы
        soup = BeautifulSoup(result.text, 'html.parser')        # Парсим страницу
        results = soup.find_all('div', {'class': 'vacancy-serp-item__layout'})  # Получаем все вакансии с страницы
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_hh_jobs(keywords):
    url = f'https://lobnya.hh.ru/search/vacancy?text={keywords}&items_on_page=20&search_period=1'
    max_page = extract_max_pages(url)
    jobs = extract_jobs(max_page, url)
    return jobs