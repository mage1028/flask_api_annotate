from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request
from flask_httpauth import HTTPBasicAuth
from flask_cors import *
import json
from db.db_select import *

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
CORS(app, supports_credentials=True)

parser = reqparse.RequestParser()


class HelloWorld(Resource):
    def get(self):
        data = {}
        data['currentAuthority'] = 'guest'
        data['status'] = 'ok'
        data['type'] = 'account'

        return data


api.add_resource(HelloWorld, '/')


# todo 登陆

class Login(Resource):
    def post(self, **kwargs):
        parser.add_argument('userName')
        parser.add_argument('password')
        parser.add_argument('type')

        args = parser.parse_args()

        userName = args['userName']
        password = args['password']

        user = select_user_pas(userName)
        try:
            if user[4] == password:  # 密码正确
                data = {}
                data['currentAuthority'] = user[2]
                data['status'] = 'ok'
                data['type'] = 'account'
                data['id'] = user[0]

                return data
        except:
            data = {}
            data['status'] = '0'
            return data


api.add_resource(Login, '/api/login/account')


# todo 查看任务
class Mission(Resource):
    def post(self):

        parser.add_argument('currentPage')
        parser.add_argument('pageSize')
        parser.add_argument('sorter')
        parser.add_argument('status')

        args = parser.parse_args()

        currentPage = args['currentPage']
        pageSize = args['pageSize']
        sorter = args['sorter']
        status = args['status']

        print(status, 'aaaa', type(status), type(sorter))
        if currentPage == None:
            currentPage = 1
            pageSize = 10
        if status == '':
            status = None
        res = select_mission(currentPage, pageSize, sorter, status)
        return res

    def get(self):
        parser.add_argument('currentPage')
        parser.add_argument('pageSize')
        parser.add_argument('sorter')
        parser.add_argument('status')

        args = parser.parse_args()

        currentPage = args['currentPage']
        pageSize = args['pageSize']
        sorter = args['sorter']
        status = args['status']
        if currentPage == None:
            currentPage = 1
            pageSize = 10
        res = select_mission(currentPage, pageSize, sorter, status)
        return res


api.add_resource(Mission, '/api/mission')


class User(Resource):
    def get(self):
        user = select_user_all()
        return user


api.add_resource(User, '/api/user')


class addMission(Resource):
    def post(self):
        parser.add_argument('missionKey')
        parser.add_argument('userKey')
        args = parser.parse_args()

        missionKey = json.loads(args['missionKey'])
        userKey = json.loads(args['userKey'])

        print(missionKey, userKey)
        add_mission(userKey, missionKey)
        print('insert ok')
        return 1


api.add_resource(addMission, '/api/addMission')


class CurrentUser(Resource):
    def get(self, id):
        user = select_user(id)
        return user


api.add_resource(CurrentUser, '/api/currentuser/<int:id>')


class CurrentMission(Resource):
    def get(self, id):
        data = select_mission_cur(id)

        return data


api.add_resource(CurrentMission, '/api/currentmission/<int:id>')


class Next(Resource):
    def get(self, id):
        next(id)
        return 1


api.add_resource(Next, '/api/next/<int:id>')


class Submit(Resource):
    def post(self):
        parser.add_argument('inputValue_aim')
        parser.add_argument('inputValue_danger')
        parser.add_argument('inputValue_confirm')
        parser.add_argument('inputValue_trust')
        parser.add_argument('inputValue_rely')
        parser.add_argument('time')
        parser.add_argument('type')
        parser.add_argument('id')
        parser.add_argument('userID')
        args = parser.parse_args()
        inputValue_aim = args['inputValue_aim']
        inputValue_danger = args['inputValue_danger']
        inputValue_confirm = args['inputValue_confirm']
        inputValue_trust = args['inputValue_trust']
        inputValue_rely = args['inputValue_rely']

        time = args['time']
        type = args['type']
        id = args['id']
        userID = args['userID']

        insert_avg_anno(id, inputValue_danger, inputValue_aim, inputValue_confirm, inputValue_rely, inputValue_trust,
                        type, time)
        insert_userHis(userID, id, inputValue_danger, inputValue_aim, inputValue_confirm, inputValue_rely,
                       inputValue_trust,
                       type, time)

        return 1


api.add_resource(Submit, '/api/submit')


class beginAnno(Resource):
    def post(self):
        parser.add_argument('mission')
        parser.add_argument('userID')
        args = parser.parse_args()
        mission = args['mission']
        userID = args['userID']
        change_flag(userID, mission)
        print('ok')
        return 1


api.add_resource(beginAnno, '/api/beginAnno')


class addMissionRandom(Resource):
    def post(self):
        parser.add_argument('user')
        parser.add_argument('count')
        args = parser.parse_args()
        user = json.loads(args['user'])
        count = args['count']
        add_mission_random(count,user)
        return 1
api.add_resource(addMissionRandom, '/api/addMissionRandom')

class fetchMission(Resource):
    def get(self,id):
        data=fetch_mission(id)
        return data
api.add_resource(fetchMission, '/api/fetchMission/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
