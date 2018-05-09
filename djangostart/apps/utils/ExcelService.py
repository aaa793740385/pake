# _*_coding:utf-8_*_
import os
import pymongo
import xlwt


def outputExcel(task_id):
    client = pymongo.MongoClient("127.0.0.1", 27017)
    dict = []
    try:
        db = client.crawlData  # 连接test数据库
        collection = db.taobao  # 访问test数据库中things集合

        # print collection.find({"price" : 15.80})
        # db.users.find({}, {"username" : 1, "email" : 1})
        for m in collection.find({"task_id": task_id}):  # 到时候改这里，改成根据id查找
            # print 1
            del m['_id']
            dict.append(m)
    except:
        pass
    finally:
        client.close()

    # 创建excel工作表
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # 设置表头
    worksheet.write(0, 0, label='comment')
    worksheet.write(0, 1, label='title')
    worksheet.write(0, 2, label='price')
    worksheet.write(0, 3, label='now_price')
    worksheet.write(0, 4, label='link')
    worksheet.write(0, 5, label='address')
    worksheet.col(1).width = 20000
    worksheet.col(2).width = 6000
    worksheet.col(4).width = 12000

    # print dict

    # 变量用来循环时控制写入单元格
    val0 = 1
    val1 = 1
    val2 = 1
    val3 = 1
    val4 = 1
    val5 = 1
    for list_item in dict:
        for key, value in list_item.items():
            if key == "comment":
                worksheet.write(val0, 0, value)
                val0 += 1
            elif key == "title":
                worksheet.write(val1, 1, value)
                val1 += 1
            elif key == "price":
                worksheet.write(val2, 2, value)
                val2 += 1
            elif key == "now_price":
                worksheet.write(val3, 3, value)
                val3 += 1
            elif key == "link":
                worksheet.write(val4, 4, value)
                val4 += 1
            elif key == "address":
                worksheet.write(val5, 5, value)
                val5 += 1

    # 保存
    workbook.save("downloads/excel/crawl"+task_id+".xls")


def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break


