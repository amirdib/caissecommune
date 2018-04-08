from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import numpy as np
import json
from datetime import datetime

urls = ['https://www.lepotcommun.fr/pot/qwgkeart', 'https://www.leetchi.com/fr/Cagnotte/31978353/a8a95db7', 'https://www.lepotcommun.fr/pot/w6md18bt', 'https://www.lepotcommun.fr/pot/69p7sald']
# a discuter :
# sncf = ['https://www.lepotcommun.fr/pot/solidarite-financiere']
# a verifier :
# poste = ['https://www.lepotcommun.fr/pot/vv0k4u61']


def read_data(path='data.json'):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    except(FileNotFoundError):
        print('err File not Found')
        return []

def write_data(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    path = 'data.json'
    data = []
    for url in urls:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()

        soup = BeautifulSoup(page, 'html.parser')

        participants = '0'
        funds = '0'
        domain = urlparse(url).netloc

        if domain == 'www.lepotcommun.fr' :
            funds_box = soup.findAll('span', attrs={'class': 'pink-color'})
            participants = funds_box[0].text.strip()
            funds = funds_box[1].text.strip()
        elif domain == 'www.leetchi.com' :
            funds_box = soup.findAll('h1', attrs={'class': 'o-article-status__heading'})
            funds = funds_box[0].text.strip()
            p_box = soup.findAll('span', attrs={'class': 'c-status__counter'})
            participants = p_box[1].text.strip()
        else:
                pass

        try:
            participants = int(participants)
            funds = float(re.sub('[^\d\.]', '', funds.replace(',', '.')))
            data.append([participants, funds])
        except:
             print ('err')


    sums = np.sum(data, axis=0)

    output = {}
    output['date'] = str(datetime.now())
    output['list'] = data
    output['sums'] = sums.tolist()


    print(output)

    data = read_data(path)
    print(data)
    write_data(data + [output], path)
    data.append(output)
