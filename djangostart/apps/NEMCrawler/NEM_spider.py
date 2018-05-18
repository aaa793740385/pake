# _*_encoding:utf-8_*_
# coding=utf-8
import re
import jieba
import pymongo
from pyecharts import Bar, Pie
import requests
from message.models import CloudMusicInformation


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class NEM_spider(object):
    def __init__(self):
        self.headers = {
            'host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent':
                ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                 ' (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
        }
        self.cookies = {'appver': '1.5.2'}


    # #Getting playlist (歌单)
    # def get_playlist_detail(self, playlist_id):
    #     url = 'http://music.163.com/api/playlist/detail'
    #     payload = {'id': playlist_id}
    #
    #     r = requests.get(url, params = payload, headers = self.headers,
    #         cookies=self.cookies)
    #
    #     playlist_detail = r.json()['result']['tracks']
    #
    #     return playlist_detail
    #
    # def from_playlist_get_song_list(self, playlist_id):
    #     playlist_detail = self.get_playlist_detail(playlist_id)
    #     songlist = []
    #     for song_detail in playlist_detail:
    #         song = {}
    #         song['id'] = song_detail['id']
    #         song['name'] = song_detail['name']
    #         artists_detail = []
    #         for artist in song_detail['artists']:
    #             artist_detail = {}
    #             artist_detail['name'] = artist['name']
    #             artist_detail['id'] = artist['id']
    #             artists_detail.append(artist_detail)
    #         song['artists'] = artists_detail
    #         songlist.append(song)
    #
    #     return songlist

    #获得该歌手热门的歌曲
    def get_artists_songlist(self, artist_id):
        url = 'http://music.163.com/api/artist/{}'.format(artist_id)

        r = requests.get(url, headers=self.headers, cookies=self.cookies)
        hotSongs = r.json()['hotSongs']

        songlist = []
        for hotSong in hotSongs:
            song = {}
            songlist.append(hotSong['id'])#将歌曲压进去

        return songlist

    #获得歌词
    def get_song_lyric(self, song_id):
        url = 'http://music.163.com/api/song/lyric'
        payload = {
            'os': 'pc', # osx
            'id': song_id,
            'lv': -1,
            'kv': -1,
            'tv': -1
        }

        r = requests.get(url, params=payload, headers=self.headers,
                         cookies=self.cookies)

        result = r.json()
        #print(result)
        if ('nolyric' in result) or ('uncollected' in result):
            return None
        elif 'lyric' not in result['lrc']:
            return None
        else:
            #print result['lrc']['lyric']
            return result['lrc']['lyric']
    # 清理数据
    def format_content(self,content):
        content = content.replace(u'\xa0', u' ')
        content = re.sub(r'\[.*?\]', '', content)
        # content = re.sub(r'\s*作曲.*\n', '', content)
        # content = re.sub(r'\s*作词.*\n', '', content)
        content = re.sub(r'.*：', '', content)
        content = re.sub(r'.* :', '', content)
        content = content.replace('\n', ' ')

        return content


def plot_chart(star_name, user_id, counter, chart_type='Bar'):
    items = [item[0] for item in counter]
    values = [item[1] for item in counter]
    if chart_type == 'Bar':
        chart = Bar(star_name + u'词频统计')
        chart.add(u'词频', items, values, is_more_utils=True)
        chart.height = 800
        chart.width = 1500
        chart.show_config()
        chart.render('static/bars/bar' + str(user_id) + '.html')
    # else:
    #     chart = Pie('')     #因为会遮住图像,所以这里的文字隐藏
    #     chart.add('词频', items, values, is_label_show=True, is_more_utils=True)
    #     chart.height = 800
    #     chart.width = 1500
    #     chart.show_config()
    #     chart.render('templates/p' + str(user_id) + '.html')


def startCrawlMusic(star_id,user_id):
    spider = NEM_spider()
    client = pymongo.MongoClient("127.0.0.1", 27017)
    db = client.crawlData  # 连接test数据库
    collection = db.artists  # 访问test数据库中things集合
    try:
        if not star_id.isdigit():
            artist = collection.find_one({"name": star_id})
        else:
            artist = collection.find_one({"_id": star_id})
    except:
        pass
    finally:
        client.close()

    star_id = artist[u'_id']
    star_name = artist[u'name']
    list = spider.get_artists_songlist(int(star_id))
    f = open("apps/NEMCrawler/data/lyric_list" + str(user_id) + ".txt", 'w')
    for i in range(len(list)):
        a = spider.get_song_lyric(list[i])
        if a==None:
            break
        lyric = str(spider.format_content(a))
        f.write(lyric +'\n')
    f.close()

    file = open('apps/NEMCrawler/data/lyric_list' + str(user_id) + '.txt', 'r')
    lyric_str = file.read()
    seg = jieba.cut(lyric_str)  # jieba分词
    word_list = []
    word_dict = {}
    list = []
    for each in seg:
        if len(each) > 1 and each != star_name:  # 过滤长度为1的词
            word_list.append(each)  # 加入到词语列表中

    for index in word_list:  # 遍历词语列表
        if index in word_dict:
            word_dict[index] += 1  # 根据字典键访问键值，如果该键在字典中，则其值+1
        else:
            word_dict[index] = 1  # 如果键不在字典中，则设置其键值为1

    sorted(word_dict.items(), key=lambda e: e[1], reverse=True)  # 降序key,value
    count = 0  # 计数器,只要前15个
    fc = open("apps/NEMCrawler/data/fenci" + str(user_id) + ".txt", 'w')
    for item in sorted(word_dict.items(), key=lambda e: e[1], reverse=True):  # 将歌词和频次写到txt文本中
        if count < 20:
            fc.write(item[0] + str(item[1]) + '\n')  # 将分词词频输出到txt文本中
            list.append(item[0])
            list.append(item[1])
        else:
            break
        count += 1
    fc.close()
    list1 = []
    for i in range(0, 39, 2):
        a = (list[i], list[i + 1])
        list1.append(a)
    plot_chart(star_name, user_id, list1, "Bar")
    CloudMusicInformation.objects.create(user_id=user_id, star_id=star_id, star_name=star_name)


