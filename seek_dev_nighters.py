import requests
import pytz
import datetime


def get_load_data_api(url, **kwargs):
    response = requests.get(url, params=kwargs)
    if response.ok:
        return response.json()


def load_attempts(url):
    page = 1
    number_of_pages = 1
    while page <= number_of_pages:
        content = get_load_data_api(url, page=page)
        for attempt in content['records']:
            yield attempt
        number_of_pages = content['number_of_pages']
        page += 1


def is_midnighter(attempt):
    attempt_date = datetime.datetime.fromtimestamp(
        attempt['timestamp'],
        pytz.timezone(attempt['timezone'])
    )
    midnite_hour = 0
    morning_hour = 5
    return midnite_hour <= attempt_date.hour <= morning_hour


def get_midnighters(url):
    midnighters = []
    for attempt in load_attempts(url):
        if is_midnighter(attempt):
            midnighters.append(attempt['username'])
    return midnighters


def print_midnighters(midnighters):
    if midnighters:
        print('Sent tasks to check after 24:00 the following users:')
        print('\n'.join(set(midnighters)))
    else:
        print('Midnighters not found!')


if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/'
    try:
        midnighters = get_midnighters(url)
    except requests.exceptions.ConnectionError:
        exit('NO CONNECTION!')
    print_midnighters(midnighters)
