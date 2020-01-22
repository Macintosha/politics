import datetime
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.politico.com/politics'
CHECK_WORDS = ['Democrat', 'Republican', 'GOP']
SECONDS = 86400
time_start = time.time()


def check_list(text):
    for word in CHECK_WORDS:
        if word in text:
            return True
        else:
            pass
    return False


def parser():
    articles = list()
    all_titles = list()
    session = requests.session()
    start_time = datetime.datetime.now() - datetime.timedelta(hours=15)
    flag_work = True
    while flag_work:
        request = session.get(BASE_URL)
        if request.status_code == 200:
            soup = BeautifulSoup(request.content, 'html.parser')
            divs = soup.find_all('div', class_='summary')
            for div in divs:
                try:
                    post_time = datetime.datetime.strptime(div.find('time').text[:-4], '%m/%d/%Y %I:%M %p')
                    title = div.find('a').string
                    text = div.find('div', class_='tease').text[1:-1]
                    author = div.find('p').text[21:-1]
                    link = div.find('a')['href']
                    print(f'time {time.time() - time_start}')
                    flag_check = (check_list(title) or check_list(text))
                    flag = (start_time < post_time) and (title not in all_titles) and flag_check
                    if flag:
                        articles.append({
                            'title': title,
                            'text': text,
                            'link': link,
                            'author': author,
                            'post_time': post_time})

                        f = open(f'{title}.html', 'wb')
                        f.write(requests.get(link).content)
                        f.close()
                        all_titles.append(title)
                except AttributeError:
                    time.sleep(1)

        if time.time() - time_start > SECONDS:
            flag_work = False

        print('sleep')
        time.sleep(3600)
    else:
        print('no')
    print(all_titles)


if __name__ == '__main__':
    parser()
