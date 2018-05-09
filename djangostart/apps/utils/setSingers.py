# *-* coding:utf-8 *-*
import requests
from requests.exceptions import RequestException
from lxml import etree
from pymongo import MongoClient
from concurrent import futures

CATS = {
            '1001': '华语男歌手',
            '1002': '华语女歌手',
            '1003': '华语组合/乐队',
            '2001': '欧美男歌手',
            '2002': '欧美女歌手',
            '2003': '欧美乐队/组合',
            '6001': '日本男歌手',
            '6002': '日本女歌手',
            '6003': '日本乐队/组合',
            '7001': '韩国男歌手',
            '7002': '韩国女歌手',
            '7003': '韩国乐队/组合',
            '4001': '其他男歌手',
            '4002': '其他女歌手',
            '4003': '其他乐队/组合'
        }

def get_artists(args):
    '''
    根据不同参数请求不同页面，并返回歌手信息
    :param args: 
    :return: 
    '''
    url = 'http://music.163.com/discover/artist/cat?id={}&initial={}'.format(args[0],args[1])
    result = fetch(url)
    if result is not None:
        artists = parse(result,args[0])
    return artists

def fetch(url):
    '''
    请求连接，成功时（200）返回页面内容
    :param url: 
    :return: 
    '''
    try:
        resp = requests.get(url)
    except RequestException:
        return None
    if resp.status_code == 200:
        return resp.text
    else:
        return None

def parse(page,cat_id):
    '''
    页面解析，返回当前页面所有的歌手信息
    :param page: 
    :param cat_id: 
    :return: 
    '''
    html = etree.HTML(page)
    ul = html.xpath('//ul[@id="m-artist-box"]')
    lis = ul[0].xpath('li')
    artists = []
    for li in lis:
        tmp = {}
        href = li.xpath('a|p/a')
        tmp['cat'] = CATS[cat_id]
        tmp['name'] = href[0].text
        # 使用'_id'存储歌手的id，能够保证插入数据的唯一性
        tmp['_id'] = href[0].attrib['href'].split('=')[1]
        # 如果歌手有主页的话，添加主页的信息
        if len(href) == 2:
            tmp['userhome'] = href[1].attrib['href']
        else:
            tmp['userhome'] = None
        artists.append(tmp)
    return artists

def get_args(hot=False):
    '''
    根据hot生成请求参数
    :param hot: 
    :return: 
    '''
    if hot is False:
        initials = [i for i in range(65, 91)]
        initials.append(0)
    else:
        initials = [-1]
    return [[cat_no,initial] for cat_no in CATS.keys() for initial in initials]

def get_all_artists(hot=False):
    '''
    1. 初始化请求参数
    2. 初始化存储信息
    3. 获取并保存
    :param hot: 
    :return: 
    '''
    args = get_args(hot)

    client = MongoClient()
    db = client['crawlData']

    artists = db['artists']


    # 多线程下载，用时约24秒
    with futures.ThreadPoolExecutor(4) as executor:
        res = executor.map(get_artists,args)
    for result in res:
        try:
            artists.insert_many(result)
        except:
            pass

    # 单线程下载，用时约1分33秒
    # for arg in args:
    #     result = get_artists(arg)
    #     try:
    #         artists.insert_many(result)
    #     except:
    #         pass


if __name__ == '__main__':

   get_all_artists()
   print "Done"