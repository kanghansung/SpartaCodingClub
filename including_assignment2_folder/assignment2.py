import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

songList = soup.select('a.title.ellipsis')
singerList = soup.select('a.artist.ellipsis')

count = 0
for song in songList:
    singer = singerList[count].text
    count += 1
    doc = {
        'rank':count,
        'title':song.text,
        'singer':singer
    }

    db.songs.insert_one(doc)
    print('insert ==>',count)

dataList = list(db.songs.find())
for data in dataList:
    print('rank:',data['rank'],'title:',data['title'],'singer:',data['singer'])

