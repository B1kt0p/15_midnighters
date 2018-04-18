import requests
import pytz
import datetime


def get_load_data_api(url, **kwargs):
    try:
        response = requests.get(url, params=kwargs)
        if response.ok:
            return response.json()
    except requests.exceptions.ConnectionError:
        return False


def load_attempts(url):
    page = 1
    content = get_load_data_api(url, page=page)
    if content is False:
        return False
    while content:
        for attempt in content['records']:
            yield attempt
        page += 1
        content = get_load_data_api(url, page=page)


def is_midnighter(attempt):
    attempt_date = datetime.datetime.fromtimestamp(
        int(attempt['timestamp']),
        pytz.timezone(attempt['timezone'])
    )
    midnite_hour = 0
    morning_hour = 5
    if midnite_hour <= attempt_date.hour <= morning_hour:
        return True
    else:
        return False


def print_midnighters(midnighters):
    if midnighters:
        print('Sent tasks to check after 24:00 the following users:')
        print('\n'.join(set(midnighters)))
        return True
    else:
        print('Midnighters not found!')


if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/?'
    midnighters = []
    attempt_list = list(load_attempts(url))
    if not attempt_list:
        exit('Can not load data page!')
    for attempt in attempt_list:
        if is_midnighter(attempt):
            midnighters.append(attempt['username'])
    print_midnighters(midnighters)
