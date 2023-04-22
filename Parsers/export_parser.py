import csv

def save_to_csv(jobs):
    file = open(f'jobs.csv', mode='w')
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'location', 'link'])
    for job in jobs:
        writer.writerow(list(job.values()))
    return 

'''
open - открытие файла, 
Режимы:
r - чтение
w - запись (перезапись) (если файл не существует, то он создается автоматически)
'''