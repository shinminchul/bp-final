from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import data


app = Flask(__name__)
api = Api(app)

class Main(Resource):
    '''
    그냥 웹을 통해 접근했을 때 보여줄 화면을 처리한다.
    '''
    def get(self):
        return {'message' : 'Business Programming Final Exam API Server Ready. Check API Reference'}


class Checkyourkey(Resource):
    '''
    학번, 이름을 입력받고, 입력받은 키에 해당하는 인증번호(3자리)를 넘겨준다.
    '''
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required = True)
        parser.add_argument('stuno', type=int, required = True)
        args = parser.parse_args()
        stuno = args['stuno']
        name = args['name']
        if stuno in list(data.user_data['name'].keys()):
            if data.user_data['name'][stuno] == name:
                return {'result': 'Authorized',
                        'message': 'Your Key is {0}'.format(data.user_data['key'][stuno])}
            else:
                return {'result': 'Authorization Failed!',
                        'message': 'Please Check Your Input. Something Wrong - Your Input is {0} - {1}'.format(stuno, name)}
        else:
            return {'result': 'Authorization Failed!',
                    'message': 'Please Check Your Input. Something Wrong - Your Input is {0} - {1}'.format(stuno, name)}

class Get_Baseball(Resource):
    '''
    학번, 이름을 입력받고, 입력받은 키에 해당하는 인증번호(3자리)를 넘겨준다.
    '''
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('key', type=int, location = 'headers',required = True)
        args = parser.parse_args()
        key = args['key']
        if key in list(data.user_data['key'].values()):
            return {'result': 'Authorized',
                    'data': data.baseball_data}
        else:
            return {'result': 'Authorization Failed!',
                    'message': 'Your Key is not Registered. Please Check Again'}

api.add_resource(Main, '/')
api.add_resource(Checkyourkey, '/user')
api.add_resource(Get_Baseball, '/data')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
