# _*_coding:utf-8_*_

import pymongo
from pyecharts import Geo

citys = {u"海门", u"鄂尔多斯", u"招远", u"舟山", u"齐齐哈尔", u"盐城", u"赤峰", u"青岛", u"乳山", u"金昌", u"泉州", u"莱西", u"日照", u"胶南", u"南通",
         u"拉萨", u"云浮", u"梅州", u"文登", u"上海", u"攀枝花", u"威海", u"承德", u"厦门", u"汕尾", u"潮州", u"丹东", u"太仓", u"曲靖", u"烟台",
         u"福州", u"瓦房店", u"即墨", u"抚顺", u"玉溪", u"张家口", u"阳泉", u"莱州", u"湖州", u"汕头", u"昆山", u"宁波", u"湛江", u"揭阳", u"荣成",
         u"连云港", u"葫芦岛", u"常熟", u"东莞", u"河源", u"淮安", u"泰州", u"南宁", u"营口", u"惠州", u"江阴", u"蓬莱", u"韶关", u"嘉峪关", u"广州",
         u"延安", u"太原", u"清远", u"中山", u"昆明", u"寿光", u"盘锦", u"长治", u"深圳", u"珠海", u"宿迁", u"咸阳", u"铜川", u"平度", u"佛山", u"海口",
         u"江门", u"章丘"
                u"肇庆", u"大连", u"临汾", u"吴江", u"石嘴山", u"沈阳", u"苏州", u"茂名", u"嘉兴", u"长春", u"胶州", u"银川", u"张家港", u"三门峡",
         u"锦州", u"南昌", u"柳州", u"三亚", u"自贡", u"吉林", u"阳江", u"泸州", u"西宁", u"宜宾", u"呼和浩特", u"成都", u"大同", u"镇江", u"桂林",
         u"张家界", u"宜兴", u"北海", u"西安", u"金坛", u"东营", u"牡丹江", u"遵义", u"绍兴", u"扬州", u"常州", u"潍坊", u"重庆", u"台州", u"南京",
         u"滨州", u"贵阳", u"无锡", u"本溪", u"克拉玛依", u"渭南", u"马鞍山", u"宝鸡", u"焦作", u"句容", u"北京", u"徐州", u"衡水", u"包头", u"绵阳",
         u"乌鲁木齐", u"枣庄", u"杭州", u"淄博", u"鞍山", u"溧阳", u"库尔勒", u"安阳", u"开封", u"济南", u"德阳", u"温州", u"九江", u"邯郸", u"临安",
         u"兰州", u"沧州", u"临沂", u"南充", u"天津", u"富阳", u"泰安", u"诸暨", u"郑州", u"哈尔滨", u"聊城", u"芜湖", u"唐山", u"平顶山", u"邢台",
         u"德州", u"济宁", u"荆州", u"宜昌", u"义乌", u"丽水", u"洛阳", u"秦皇岛", u"株洲", u"石家庄", u"莱芜", u"常德", u"保定", u"湘潭", u"金华",
         u"岳阳", u"长沙", u"衢州", u"廊坊", u"菏泽", u"合肥", u"武汉", u"大庆"}


def mapMaking(task_id):
    client = pymongo.MongoClient("127.0.0.1", 27017)
    list = []
    dict = {}
    list1 = []
    try:
        db = client.crawlData  # 连接test数据库
        collection = db.taobao  # 访问test数据库中things集合
        for m in collection.find({"task_id": task_id}, {"address": 1, "_id": 0}):
            if m['address'] in citys:
                list.append(m['address'])
    except:
        pass
    finally:
        client.close()
    # print list

    # 生成关系，查找键值
    for index in list:  # 遍历词语列表
        if index in dict:
            dict[index] += 1  # 根据字典键访问键值，如果该键在字典中，则其值+1
        else:
            dict[index] = 1  # 如果键不在字典中，则设置其键值为1

    # print dict      #{u'\u4e0a\u6d77': 1, u'\u9633\u6c5f': 6, u'\u6210\u90fd': 1, u'\u91d1\u534e': 1}
    for item in dict.items():  # 化成列表类型
        list1.append(item[0])
        list1.append(item[1])

    # print len(list1)
    list2 = []

    for i in range(0, len(list1), 2):  # 拼成pycharts能够输入的格式,步长为2
        a = (list1[i], list1[i + 1])
        list2.append(a)

    data = list2
    geo = Geo(u"商品在全国售卖主要城市", u"商品", title_color="#fff",
              title_pos="center", width=1000,
              height=600, background_color='#404a59')
    geo.height = 800
    geo.width = 1500
    attr, value = geo.cast(data)
    geo.add("", attr, value, visual_range=[0, 200], maptype='china', visual_text_color="#fff",
            symbol_size=10, is_visualmap=True)
    geo.render("static/maps/map" + task_id + ".html")  # 生成html文件






