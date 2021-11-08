import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd
from data_preparation import get_states_urls, get_area, get_capital, get_date_admitted, get_income, get_population


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('states.log')
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def main():
    failed_counter = 0
    success_counter = 0
    failed_idx = []
    states_info = []

    states_urls = get_states_urls()
    for idx in range(states_urls.shape[0]):
        state = states_urls.iloc[idx, :].state
        url = states_urls.iloc[idx, :].url

        soup = bs(requests.get(url).text, features='lxml')
        table = soup.find('table', class_='infobox')

        try:
            state_info = {
                            'name':state,
                            'capital':get_capital(table),
                            'date_admitted':get_date_admitted(table),
                            'population':get_population(table),
                            'area':get_area(table),
                            'income':get_income(table)
                            }
        except:
            logger.exception(f'{idx}.{state} - Failed Scraping')
            print('\n')
            failed_counter += 1
            failed_idx.append(idx)
            continue
        
        else:
            success_counter += 1
            states_info.append(state_info)
            logger.debug(f'{idx}.{state} - Successful scraping process')
            print('\n')
        
    states_info = pd.DataFrame(states_info)
    states_info.to_csv('us_states.csv', index=False)

    print('Summary of the scrapping process:')
    print(f'\t Number of successful scraping processes: {success_counter}')
    print(f'\t Number of failed scraping processes: {failed_counter} at indices: {failed_idx}')

    return states_info

if __name__ == '__main__':
    main()