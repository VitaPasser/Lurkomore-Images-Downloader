from functools import partial

import requests
from bs4 import BeautifulSoup
import os
import multiprocessing


class Config:
    link_general = 'https://lurkmore.pro'
    directory_images = './images'


def save_html(link, filename):
    response = requests.get(link).text

    with open(filename, 'wt', encoding='utf-8') as file:
        file.write(response)


def take_links_on_category():
    with open('lurksite.html', 'rt', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
        block = soup.find('div', id="target-list")
        links = block.find_all('a')
        return [link['href'] for link in links]


def take_links_on_article(filename):
    with open(filename, 'rt', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
        block = soup.find('div', class_='mw-category mw-category-columns')
        links = block.find_all('a')
        return [link['href'] for link in links]


def take_links_in_name_article(filename):
    with open(filename, 'rt', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
        block = soup.find('div', class_='mw-parser-output')
        links = block.find_all('a', class_='mw-redirect')
        return [link['href'] for link in links]


def take_links_on_img_article(link):
    response = requests.get(link).text

    soup = BeautifulSoup(response, 'lxml')
    block = soup.find('div', class_='mw-parser-output')
    images = block.find_all('a', class_='mw-file-description')
    for aa in images:
        print(aa['href'])
    return [img['href'] for img in images]


def take_link_full_image(link):
    response = requests.get(link).text

    soup = BeautifulSoup(response, 'lxml')
    block = soup.find('div', class_='fullImageLink')
    link = block.find('a')['href']

    return link


def main(directory_images):
    if not os.path.exists('./lurksite.html'):
        save_html(Config.link_general, 'lurksite.html')

    if not os.path.exists('./categories'):
        os.mkdir('./categories')

    links = take_links_on_category()

    links2 = []
    for link in links:
        print(link)
        if not os.path.exists('./categories' + link.replace(':', '-')):
            print('download')
            os.mkdir('./categories' + link.replace(':', '-'))
            save_html(Config.link_general + link,
                      './categories' + link.replace(':', '-') + link.replace(':', '-') + '.html')
        else:
            print('exist')

        if link == '/Имена':
            links2.append(
                take_links_in_name_article('./categories' + link.replace(':', '-') + link.replace(':', '-') + '.html'))
        else:
            links2.append(
                take_links_on_article('./categories' + link.replace(':', '-') + link.replace(':', '-') + '.html'))

    if not os.path.exists(directory_images):
        os.mkdir(directory_images)

    links = []
    for links3 in links2:
        for links1 in links3:
            links.append(links1)

    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as process:
        process.map(partial(download, directory_images=directory_images), links[:20])


def download(link, directory_images):
    print("==article==")
    print(link)

    if link[1:] == '404':
        print('Пропуск, ПИДОРЫ БЛЯДЬ, КААК СМЕШНО СУКА!')
        return

    links_on_img = take_links_on_img_article(Config.link_general + link)
    print("==images==")
    for link1 in links_on_img:
        print(link1)
        result = take_link_full_image(Config.link_general + link1)
        download_img(Config.link_general + result, directory_images + "/" + result.replace('/', '-'))


def download_img(link, name):
    response = requests.get(url=link)

    with open(name, 'wb') as file:
        file.write(response.content)
