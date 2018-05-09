# _*_coding:utf-8_*_
import pymongo
from pyecharts import Pie


def pricePieMaking(task_id,start_range,end_range):
    client = pymongo.MongoClient("127.0.0.1", 27017)
    list = []
    dict = {}
    list1 = []
    try:
        db = client.crawlData  # 连接test数据库
        collection = db.taobao  # 访问test数据库中things集合
        for m in collection.find({"task_id": task_id}):  # 到时候改这里，改成根据id查找

            list.append(m['now_price'])
    except:
        pass
    finally:
        client.close()
    end_range = float(end_range)
    start_range = float(start_range)
    price_range = (end_range - start_range) / 4
    price1 = str(start_range) + '~' + str(start_range + price_range)  # 1000~1250
    price2 = str(start_range + price_range) + '~' + str(start_range + price_range * 2)  # 1250~1500
    price3 = str(start_range + price_range * 2) + '~' + str(start_range + price_range * 3)  # 1500~1750
    price4 = str(start_range + price_range * 3) + '~' + str(end_range)  # 1750~2000

    dict[price1] = 0
    dict[price2] = 0
    dict[price3] = 0
    dict[price4] = 0
    # 分析数据
    for index in list:  # 遍历词语列表
        if float(index.encode("utf-8")) > start_range and float(index.encode("utf-8")) < start_range + price_range * 1:
            dict[price1] += 1
        elif float(index.encode("utf-8")) > start_range + price_range and float(
                index.encode("utf-8")) < start_range + price_range * 2:
            dict[price2] += 1
        elif float(index.encode("utf-8")) > start_range + price_range * 2 and float(
                index.encode("utf-8")) < start_range + price_range * 3:
            dict[price3] += 1
        elif float(index.encode("utf-8")) > start_range + price_range * 3 and float(index.encode("utf-8")) < end_range:
            dict[price4] += 1
        else:  # 不在这个范围内的
            continue
    # print dict

    for item in dict.items():  # 化成列表类型
        list1.append(item[0])
        list1.append(item[1])
    # print list1

    list2 = []
    for i in range(0, len(list1), 2):  # 拼成pycharts能够输入的格式,步长为2
        a = (list1[i], list1[i + 1])
        list2.append(a)

    # 生成图表
    pie = Pie(u"商品价格范围分布图")
    attr, value = pie.cast(list2)
    pie.add("", attr, value, is_label_show=True)
    # pie.show_config()
    pie.render("static/prices/price" + task_id + ".html")

