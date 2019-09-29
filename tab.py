from datetime import datetime
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import requests
import pandas as pd
import multiprocessing
from multiprocessing import Pool
import os


from html_table_parser import HTMLTableParser
 
url = 'https://bases-brothers.ru/categories.aspx?parent='
URLS = 'urls.txt'
TABLES = 'tables.txt'

class HTMLTableParser:

    def parse_urltable(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return [(table['id'],self.parse_htmltable(table))\
                for table in soup.find_all('table')]

    def parse_urldiv(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        divtext = [soup.find('div', {'class':'BreadCrumbs'})] # Parse the div by div class.
        city = [soup.find('span', text='Все объявления в Москве')]# Parse the span.
        print(city)
        
        f = open(TABLES, 'a')
        f.write("%s\n" % divtext)
        f.close()
        return divtext
    
    def parse_htmltable(self, table):
        
        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            if len(columns) == 4: #cut yandex and other shit (!= 4) rows here
                if row_marker != 24 and row_marker != 49: #cut some empty lines here
                    rowtext = [i.text for i in columns]
                    f = open(TABLES, 'a')
                    f.write("%s\n" % rowtext)
                    # f.close() moved to end of func.
                else:
                    pass
                 
                for column in columns:
                    df.iat[row_marker,column_marker] = column.get_text()
                    column_marker += 1
                    
                if len(columns) > 0:
                    row_marker += 1
                    
            else:
                pass
                
        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
            
        f.close()
        return df
    

    def writetable(self, url):
        i = 0
        try:
            
            table = self.parse_urltable(url)[0][1] # Grabbing the table from the tuple
            print(table.head())
            # only if table is passed, then try to grab htmls div:
            print(self.parse_urldiv(url))
            i += 1
            
        except:
            print('pass')
            i += 1
            pass
        
        return i

#Чтение из файла
def readlinks(file):
    with open(createif(file)) as f:
        lines = f.read().splitlines()
    return lines

#Проверка файла на существование
def checkfile(file):
    return os.path.isfile(file)

#Создание файла если нет
def createif(file):
    if checkfile(file):
        return file
    else:
        open(file, 'a').close()
        print('Файл ' + file + ' был создан')
        return file
    
#Добавление в файл
def addlinks(file,my_list):
    with open(createif(file), 'a') as f:
        for item in my_list:
            f.write("%s\n" % item)

def main():
    hp = HTMLTableParser()
    cpucores = multiprocessing.cpu_count()
    pool = Pool(processes=cpucores + 4)
    urlpool = [url + str(i) for i in range (1, 8)] # pool of urls
    
    startTime = datetime.now().replace(microsecond=0)
    pool.map(hp.writetable, urlpool)
    endTime = datetime.now().replace(microsecond=0)
    
    print('\nTime used: ', endTime - startTime)
    
if __name__ == "__main__":
    main()
