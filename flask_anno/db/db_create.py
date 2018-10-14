import pymysql


def connect():
    connect = pymysql.connect(host='localhost', user='root', password='', db='annotate2', port=3306,
                              charset='utf8')
    return connect
