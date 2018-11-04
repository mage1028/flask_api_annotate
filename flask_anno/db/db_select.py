import pymysql
import logging
import json

#
# def connect():
#     connect = pymysql.connect(host='localhost', user='root', password='', db='annotate2', port=3306,
#                               charset='utf8')
#     return connect


def connect():
    connect = pymysql.connect(host='192.168.100.103', user='root', password='root', db='fakenewsb', port=3306,
                              charset='utf8')
    return connect


def select_user_pas(account):
    '''

    :param account: user账户
    :return: user密码
    '''
    sql = '''select * from user where account='{0}'
    '''.format(account)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchone()
        return data
    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        logging.exception(e)


def select_user_info(id):
    '''

    :param account: user账户
    :return: user密码
    '''
    sql = '''select * from user where id='{0}'
    '''.format(id)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchone()
        return data
    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        logging.exception(e)


def select_mission(currentPage, pageSize, sorted, status):
    '''

    :param currentPage:
    :param pageSize:
    :param sorted:
    :param status:
    :return: 找出指定的数据
    '''
    print(currentPage, pageSize, sorted, status)
    begin = (int(currentPage) - 1) * int(pageSize)
    if sorted == 'callNo_descend' and status == '0':  # 根据标记次数降序
        sql = '''select id,content,annoCount from annoText where annoCount>=20 order by annoCount desc limit {0},{1}
           '''.format(begin, pageSize)
    if sorted == 'callNo_descend' and status == '1':  # 根据标记次数降序
        sql = '''select id,content,annoCount from annoText where annoCount<20 order by annoCount desc limit {0},{1}
           '''.format(begin, pageSize)
    if sorted == 'callNo_ascend' and status == '1':  # 根据标记次数降序
        sql = '''select id,content,annoCount from annoText where annoCount<20 order by annoCount asc limit {0},{1}
            '''.format(begin, pageSize)
    if sorted == 'callNo_ascend' and status == '0':  # 根据标记次数降序
        sql = '''select id,content,annoCount from annoText where annoCount>=20 order by annoCount asc limit {0},{1}
              '''.format(begin, pageSize)
    if sorted == 'callNo_ascend' and status == None:  # 根据标记次数降序
        sql = '''select id,content,annoCount from annoText order by annoCount asc limit {0},{1}
              '''.format(begin, pageSize)
    if sorted == 'callNo_descend' and status == None:  # 根据标记次数降序
        sql = '''select id,content,annoCount from annoText order by annoCount desc limit {0},{1}
           '''.format(begin, pageSize)
    if status == '0' and sorted == None:  # 根据标记次数降序
        sql = '''select id,content,annoCount from annoText where annoCount>=20 order by annoCount asc limit {0},{1}
              '''.format(begin, pageSize)
    if status == '1' and sorted == None:  # 根据标记次数降序
        sql = '''select id,content,annoCount from annoText where annoCount<20 order by annoCount asc limit {0},{1}
              '''.format(begin, pageSize)
    if status == None and sorted == None:
        sql = '''select id,content,annoCount from annoText limit {0},{1}
        '''.format(begin, pageSize)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchall()

        result = {}
        result['list'] = []
        result['pagination'] = {}
        for i in data:
            res = {}
            res['key'] = i[0]
            res['name'] = i[0]
            if i[2] >= 20:
                res['status'] = 0
            else:
                res['status'] = 1
            res['desc'] = i[1]
            res['callNo'] = i[2]
            res['disabled'] = False
            result['list'].append(res)

        result['pagination']['current'] = int(currentPage)
        result['pagination']['pageSize'] = int(pageSize)
        result['pagination']['total'] = int(select_mission_count())
        user = select_user_all()
        result['user'] = user

        return result
    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        logging.exception(e, sql)


def select_mission_count():
    '''

    :return: 找出全部任务
    '''
    sql = '''select count(*) from annoText

    '''
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchone()[0]

        return data
    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        logging.exception(e, sql)


def select_user_all():
    '''
    找出全部的用户
    '''
    sql = '''select * from user
    '''
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        res = []
        datas = cursor.fetchall()
        for i in datas:
            data = {}
            data['key'] = i[0]
            data['userId'] = i[0]
            data['userName'] = i[1]
            data['userType'] = i[2]
            data['userAccount'] = i[3]
            res.append(data)
        result = {}
        result['list'] = res
        return result

    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        logging.exception(e, sql)


def add_mission(user, mission):
    conn = connect()
    cursor = conn.cursor()
    for i in user:
        for j in mission:
            sql = '''insert into mission(userID,missionID)values ({0},{1})
            '''.format(i, j)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                pass


def select_user(id):
    '''

    :param id: id
    :return:
    {'id':,
    'name':,
    'account':,
    'type':,
    'mission':{}, mission missionCount missionComplete
    }
    '''
    conn = connect()
    cursor = conn.cursor()
    sql = '''select * from user where id={0}
    '''.format(id)
    user = {}
    user['datas'] = []

    try:
        cursor.execute(sql)
        res = cursor.fetchone()
        user['id'] = id
        user['name'] = res[1]
        user['account'] = res[3]
        user['type'] = res[2]
    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        logging.exception(e, sql)
    sql = '''select * from mission where userID={0}
    '''.format(id)
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        count = 0
        comp = 0
        for i in res:
            tmp = {}
            if i[3]:
                comp += 1
                tmp['isAnno'] = '已标注'

            else:
                tmp['isAnno'] = '未标注'

            tmp['id'] = i[1]
            tmp['dangerValue'] = i[2]
            tmp['rely'] = i[3]
            tmp['confirm'] = i[4]
            tmp['trust'] = i[5]
            tmp['aim'] = i[6]
            tmp['type'] = i[7]
            tmp['timeliness'] = i[8]
            try:
                tmp['time'] = i[9].strftime('%Y-%m-%d %H:%M:%S')
            except:
                tmp['time'] = i[9]

            tmp.update(select_Avg(i[1]))
            user['datas'].append(tmp)
            count += 1

        user['missionCount'] = count
        user['missionComplete'] = comp
        user['mission']=select_mission_cur(id)
        return user
    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        print(e)


def selectID_Weibo(id):
    sql = '''select * from annoText where id={0}
    '''.format(id)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = list(cursor.fetchone())
        return data
    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        logging.exception(e)


def select_mission_cur(id):
    sql = '''select * from mission where userID={0} and flag=1
    '''.format(id)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = list(cursor.fetchone())
        tmp = {}
        if data[5]:
            tmp['isAnno'] = '已标注'

        else:
            tmp['isAnno'] = '未标注'

        tmp['id'] = data[1]
        tmp['dangerValue'] = data[2]
        tmp['rely'] = data[3]
        tmp['confirm'] = data[4]
        tmp['trust'] = data[5]
        tmp['aim'] = data[6]
        tmp['type'] = data[7]
        tmp['timeliness'] = data[8]
        try:
            tmp['time'] = data[9].strftime('%Y-%m-%d %H:%M:%S')
        except:
            tmp['time'] = data[9]

        content = select_Avg(data[1])
        tmp.update(content)

        return tmp
    except Exception as e:
        logging.exception(e)
        try:
            sql2 = '''select * from mission where userID={0}
              '''.format(id)
            cursor.execute(sql2)
            data = list(cursor.fetchone())
            tmp = {}
            if data[5]:
                tmp['isAnno'] = '已标注'

            else:
                tmp['isAnno'] = '未标注'

            tmp['id'] = data[1]
            tmp['dangerValue'] = data[2]
            tmp['rely'] = data[3]
            tmp['confirm'] = data[4]
            tmp['trust'] = data[5]
            tmp['aim'] = data[6]
            tmp['type'] = data[7]
            tmp['timeliness'] = data[8]
            try:
                tmp['time'] = data[9].strftime('%Y-%m-%d %H:%M:%S')
            except:
                tmp['time'] = data[9]
            content = select_Avg(data[1])
            tmp.update(content)

            return tmp
        except Exception as e:
            logging.exception(e)


def find_missionID(id):
    sql = '''select missionID from mission where userID={0} and flag=1
    '''.format(id)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchone()[0]
        return data
    except Exception as e:
        sql = '''select missionID from mission where userID={0}
           '''.format(id)
        cursor.execute(sql)
        data = cursor.fetchone()[0]
        return data


def select_next(id, missionID):
    sql = '''SELECT missionID FROM mission WHERE userID={1} and missionID > {0} ORDER BY missionID ASC
    '''.format(missionID, id)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchone()[0]
        return data
    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        logging.exception(e)


def next(userID):
    missionID = int(find_missionID(userID))
    print(missionID)

    sql = '''update mission set flag=0 where userID={0} and missionID={1}
    '''.format(userID, missionID)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()

        new_id = select_next(userID, missionID)
        sql2 = '''update mission set flag=1 where userID={0} and missionID={1}
        '''.format(userID, new_id)
        cursor.execute(sql2)
        conn.commit()

    except Exception as e:
        conn.rollback()  # 回滚
        conn.close()
        logging.exception(e)


def select_avg_anno(id):
    '''

    :return: select平均记录
    '''
    sql = '''select danger,aim,confirm,rely,trust,type,timeliness from annoText where id ='{0}'
    '''.format(id)
    con = connect()
    cursor = con.cursor()
    try:
        cursor.execute(sql)
        res = cursor.fetchone()
        return res
    except Exception as e:
        logging.exception(e)


def judge(id):
    sql = '''select danger from annoText where id={0}
    '''.format(id)
    con = connect()
    cursor = con.cursor()
    try:
        cursor.execute(sql)
        res = cursor.fetchone()[0]

        if res == None:

            return False
        else:
            return True
    except Exception as e:
        logging.exception(e)


def insert_avg_anno(id, danger, aim, confirm, rely, trust, type, time):
    '''

    :return: 更新平均记录
    '''
    if not judge(id):
        types = {
            '政治': 0, '经济': 0, '社会': 0, '教育': 0, '科技': 0, '娱乐': 0, '军事': 0, '健康': 0,
        }
        times = {
            '存在时效性': 0, '过时': 0, '与时间无关': 0,

        }
        types[type] = 1
        times[time] = 1
        sql = '''update annoText set danger='{0}',aim='{1}',confirm='{2}',rely='{3}',trust='{4}',type='{5}',timeliness='{6}',annoCount='{7}' where id='{8}'
               '''.format(danger, aim, confirm, rely, trust, json.dumps(types, ensure_ascii=False),
                          json.dumps(times, ensure_ascii=False), 1, id)
        con = connect()
        cursor = con.cursor()
        try:
            cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(sql)
            logging.exception(e)
    else:
        result = select_avg_anno(id)
        danger = (float(result[1]) * int(result[-1]) + float(danger)) / (int(result[-1]) + 1)
        aim = (float(result[2]) * int(result[-1]) + float(aim)) / (int(result[-1]) + 1)
        confirm = (float(result[3]) * int(result[-1]) + float(confirm)) / (int(result[-1]) + 1)
        rely = (float(result[4]) * int(result[-1]) + float(rely)) / (int(result[-1]) + 1)
        trust = (float(result[5]) * int(result[-1]) + float(trust)) / (int(result[-1]) + 1)
        count = int(result[-1]) + 1
        types = json.loads(result[6])
        types[type] = int(types[type]) + 1
        times = json.loads(result[7])
        times[time] = int(times[time]) + 1
        sql = '''update annoText set danger='{0}',aim='{1}',confirm='{2}',rely='{3}',trust='{4}',type='{5}',timeliness='{6}',annoCount='{7}' where id='{8}'
        '''.format(danger, aim, confirm, rely, trust, json.dumps(types, ensure_ascii=False),
                   json.dumps(times, ensure_ascii=False), count, id)
        con = connect()
        cursor = con.cursor()
        try:
            cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(sql)
            logging.exception(e)


def insert_userHis(userID, id, danger, aim, confirm, rely, trust, type, time):
    '''


    :return: 插入更新个人历史记录
    '''
    sql = '''update mission set danger='{0}',aim='{1}',confirm='{2}',rely='{3}',trust='{4}',type='{5}',timeliness='{6}' where missionID='{7}'and userID='{8}'
    '''.format(danger, aim, confirm, rely, trust, type, time, id, userID)
    con = connect()
    cursor = con.cursor()
    try:
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        logging.exception(e)


def change_flag(userID, missionID):
    missionID_now = int(find_missionID(userID))
    print(missionID)

    sql = '''update mission set flag=0 where userID={0} and missionID={1}
        '''.format(userID, missionID_now)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()

        sql2 = '''update mission set flag=1 where userID={0} and missionID={1}
        '''.format(userID, missionID)
        cursor.execute(sql2)
        conn.commit()
    except Exception as e:
        print(e)


def add_mission_random(count, user):
    '''

    :param count:
    :param user:
    :return: 随机添加任务
    '''
    sql = '''SELECT id FROM annoText
WHERE id >= (SELECT floor(RAND() * (SELECT MAX(id) FROM annoText)))
ORDER BY id LIMIT {0};
    '''.format(count)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = list(cursor.fetchall())
        res = []
        for i in data:
            res.append(i[0])
        for i in user:
            add_mission(str(i), res)
    except Exception as e:
        logging.exception(e)


def fetch_mission(id):
    '''

    :param id:
    :return:
    {
    user:  [{id,name,记录,time}]//所有编辑过这个任务的人
    editing:[{id,name}] 正在编辑的人
    avg...
    content,
    reason,


        }
    '''

    data = selectID_Weibo(id)
    conn = connect()
    cursor = conn.cursor()

    tmp = {}
    avg = select_Avg(id)
    tmp.update(avg)
    sql = '''select * from mission where missionID={0}
    '''.format(id)
    try:

        cursor.execute(sql)
        res = cursor.fetchall()
        userAnnotated = []
        userAnnotating = []
        for i in res:

            user_info = select_user_info(i[0])
            t = {}
            t['id'] = i[0]
            t['name'] = user_info[1]
            t['userType'] = user_info[2]
            t['account'] = user_info[3]

            if i[2]:  # 如果被标注了
                t['userID'] = i[0]
                t['dangerValue'] = i[2]
                t['rely'] = i[3]
                t['confirm'] = i[4]
                t['trust'] = i[5]
                t['aim'] = i[6]
                t['type'] = i[7]
                t['timeliness'] = i[8]
                try:
                    t['time'] = i[9].strftime('%Y-%m-%d %H:%M:%S')
                except:
                    t['time'] = i[9]
                userAnnotated.append(t)
            else:
                userAnnotating.append(t)
        tmp['userAnnotated'] = userAnnotated
        tmp['userAnnotating'] = userAnnotating
        return tmp

    except Exception as e:
        logging.exception(e)


def select_Avg(id):
    '''

    :param id:
    :return: dict
    '''
    tmp = {}
    sql = '''select * from annoText where id={0}
    '''.format(id)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchone()
        tmp['reason'] = data[1]
        tmp['content'] = data[2]
        tmp['annoCount'] = str(data[3])
        tmp['dangerAvg'] = data[4]
        tmp['aimAvg'] = data[5]
        tmp['ConfirmAvg'] = data[6]
        tmp['rely'] = data[7]
        tmp['trustAvg'] = data[8]
        try:
            typeAvg = json.loads(data[9])
            tmp['typeAvg'] = typeAvg
            tmp['timelinessAvg'] = json.loads(data[10])
        except:
            tmp['typeAvg'] = {
                "政治": 0,
                "经济": 0,
                "社会": 0,
                "教育": 0,
                "科技": 0,
                "娱乐": 0,
                "军事": 0,
                "健康": 0,
            }
            tmp['timelinessAvg'] = {
                "存在时效性": 0,
                "过时": 0,
                "与时间无关": 0
            }

        return tmp
    except Exception as e:
        print('select_avg')
        logging.exception(e)


def register(account,password,name):
    sql='''insert into user(account,password,name,type)values ({0},{1},{2},'user')
    '''.format(account,password,name)
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        return 1
    except Exception as e:
        return 0
