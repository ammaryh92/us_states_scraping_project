import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from dateutil import parser
import re

def get_states_urls():
    url = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States'
    soup = bs(requests.get(url).text, features='lxml')
    states_list = soup.find('table', class_='wikitable').find('tbody').find_all('tr')[2:]
    states_urls_df_list = []
    for state in states_list:
        states_urls_df_list.append({'state':state.find('th').find('a').text, 'relative_url':state.find('th').find('a')['href']})
    states_urls_df = pd.DataFrame(states_urls_df_list)
    states_urls_df['url'] = 'https://en.wikipedia.org'+ states_urls_df['relative_url']
    states_urls_df.drop('relative_url', axis=1, inplace=True)
    return states_urls_df

def to_date(date_string):
    date = re.search(r'\w+ \d+, \d{4}', date_string)[0]
    return parser.parse(date)

def to_int(number_string):
    return int(re.search(r'[\d,]+', number_string)[0].replace(',', ''))
    
def get_capital(table):
    capital_string = table.find(text='Capital').find_next('td').text
    return re.search(r'\w+', capital_string)[0]

def get_date_admitted(table):
    date_string = table.find(text=re.compile(r'Admitted')).next.text
    return to_date(date_string)

def get_population(table):
    pop_regex = re.compile(r'Population')
    pop_text = table.find(text=pop_regex).parent.parent.next_sibling.find('td').text
    return to_int(pop_text.replace(',', ''))

def get_area(table):
    area_regex = re.compile(r'Area')
    number_string = table.find(text=area_regex).parent.parent.next_sibling.find('td').text
    return to_int(number_string)

def get_income(table):
    income_regex = re.compile(r'Median household income')
    number_string = table.find(text=income_regex).parent.parent.next_sibling.text
    return to_int(number_string)
