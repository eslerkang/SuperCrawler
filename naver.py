import requests
from bs4 import BeautifulSoup

URL = 'https://comic.naver.com/webtoon/weekday.nhn'
URL_FINISH = 'https://comic.naver.com/webtoon/finish.nhn'


def get_last_epi(content):
    result = requests.get(content['url'])
    soup = BeautifulSoup(result.text, 'html.parser')
    last_epi = soup.find(
        'div',
        {'class': 'webtoon'}
    ).find_all(
        'td',
        {'class': 'title'}
    )[0].find('a')['onclick'].split(',')[-1][1:-2]
    return last_epi


def get_id_list():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    all_toon = soup.find('div', {'class': 'daily_all'})
    contexts = all_toon.find_all('a', {'class': 'title'})

    id_list = []

    for context in contexts:
        id_list.append(context['href'].split('?')[-1].split('&')[0][8:])

    return id_list


def get_webtoon_list():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    all_toon = soup.find('div', {'class': 'daily_all'})
    contexts = all_toon.find_all('a', {'class': 'title'})
    urls = all_toon.find_all('div', {'class': 'thumb'})

    toon_dict = []

    for idx, context in enumerate(contexts):
        toon_dict.append({
            'id': context['href'].split('?')[-1].split('&')[0][8:],
            'title': context['title'],
            'url': 'https://comic.naver.com'+context['href'],
            'thumb': urls[idx].find('img')['src']
        })

    return toon_dict


def get_finish_list():
    result = requests.get(URL_FINISH)
    soup = BeautifulSoup(result.text, 'html.parser')
    all_toon = soup.find('ul', {'class': 'img_list'}).find_all('li')
    toon_list = []
    for toon in all_toon:
        em = toon.find('dt').find('em')
        if not em:
            toon_list.append(toon)
    toon_dict = []

    for toon in toon_list:
        a_tag = toon.find(
            'div',
            {'class': 'thumb'}
        ).find('a')
        url = a_tag['href']
        idx = url.split('=')[-1]
        url = 'https://comic.naver.com' + url
        thumb = a_tag.find('img')['src']
        title = a_tag['title']
        toon_dict.append({
            'id': idx,
            'title': title,
            'url': url,
            'thumb': thumb
        })
    return toon_dict


def get_finish_id_list():
    result = requests.get(URL_FINISH)
    soup = BeautifulSoup(result.text, 'html.parser')
    all_toon = soup.find('ul', {'class': 'img_list'}).find_all('li')
    toon_list = []
    for toon in all_toon:
        em = toon.find('dt').find('em')
        if not em:
            toon_list.append(toon)
    id_list = []

    for toon in toon_list:
        id_list.append(toon.find(
            'div',
            {'class': 'thumb'}
        ).find('a')['href'].split('=')[-1])

    return id_list


def get_epis(idx, last_epi):
    epi_list = []
    result = requests.get(
        f'https://comic.naver.com/webtoon/list.nhn?titleId={idx}&page=999999'
    )
    soup = BeautifulSoup(result.text, 'html.parser')
    last_page = int(
        soup.find(
            'div',
            {'class': 'paginate'}
        ).find(
            'strong',
            {'class': 'page'}
        ).find('em').string
    )
    for page in range(1, last_page+1):
        result = requests.get(
            f'https://comic.naver.com/webtoon/list.nhn?titleId={idx}&page={page}'
        )
        soup = BeautifulSoup(result.text, 'html.parser')
        trs = soup.find('table', {'class': 'viewList'}).find_all('tr')[1:]
        for tr in trs:
            if not tr.get('class'):
                title = tr.find('td', {'class': 'title'}).find('a').string
                thumb = tr.find_all('img')[0]['src']
                url = 'https://comic.naver.com' + tr.find_all('a')[0]['href']
                epi_list.append({
                    'title': title,
                    'thumb': thumb,
                    'url': url
                })
    epi_list.reverse()
    return epi_list


def get_all_img(idx, last_epi):
    img_list = []
    for epi in range(1, int(last_epi)+1):
        result = requests.get(f'https://comic.naver.com/webtoon/detail.nhn?titleId={idx}&no={epi}')
        soup = BeautifulSoup(result.text, 'html.parser')
        imgs = soup.find('div', {'class': 'wt_viewer'}).find_all('img')
        for img in imgs:
            img_list.append(img.get('src'))
    return img_list
