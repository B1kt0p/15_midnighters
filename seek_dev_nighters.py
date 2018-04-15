import requests
import pytz
import datetime


def get_load_data_api(url, **kwargs):
    try:
        response = requests.get(url, data=kwargs)
    except requests.exceptions.ConnectionError:
        return None
    if response.ok:
        return response.json()


def get_number_of_pages(url):
    content = get_load_data_api(url, data={'page':1})
    if content:
        return content['number_of_pages']


def load_attempts(url, number_of_pages):
    for page in range(1, number_of_pages+1):
        content = get_load_data_api(url, page=page)
        if content:
            for attempt in content['records']:
                yield attempt

        else:
            continue


def get_midnighters(attempt):
    attempt_date = datetime.datetime.fromtimestamp(
        int(attempt['timestamp']),
        pytz.timezone(attempt['timezone'])
    )
    midnite_hour = 0
    morning_hour = 5
    if midnite_hour <= attempt_date.hour <= morning_hour:
        return attempt['username']


def print_midnighters(midnighters):
    if midnighters:
        print('Sent tasks to check after 24:00 the following users:')
        [print(midnighter) for midnighter in midnighters]
        return True


if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/'
    number_of_pages = get_number_of_pages(url) or exit('Can not load content!')
    midnighters = []
    for attempt in load_attempts(url, number_of_pages):
        if get_midnighters(attempt):
            midnighters.append(get_midnighters(attempt))
    midnighters = tuple(set(midnighters))
    print_midnighters(midnighters) or exit('Midnighters not found!')
