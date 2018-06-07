from flask import request, jsonify
from modules.appdb import *

class Users(Resource):
    def get(self):
        jsondata = []
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from users"
        cursor.execute(query)
        for val in cursor.fetchall():
            vTmp = {}
            vTmp['id'] = val[0]
            vTmp['login'] = val[3]
            vTmp['email'] = val[5]
            vTmp['isadmin'] = val[2]
            jsondata.append(vTmp)
        return jsonify(jsondata)

    def post(self):
        conn = mysql.connect()
        cursor = conn.cursor(buffered=True)

        print(request.json)
        login = request.json['login']
        password = request.json['password']
        email = request.json['email']

        if request.json['isAdmin']:
            is_admin = request.json['isAdmin']
        else:
            is_admin = 0
        if request.json['parentID']:
            parent_id = request.json['parentID']
        else:
            parent_id = 0
        query = "insert into employees values(null,'{0}','{1}', \
                            '{2}','{3}','{4}')".format(parent_id, is_admin, login, password, email)
        cursor.execute(query)
        conn.commit()
        return {'status': 'success'}


class UsersByID(Resource):
    def get(self, user_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from users where ID = %d " % int(user_id)

        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                result = {}
                result['id'] = val[0]
                result['login'] = val[3]
                result['email'] = val[5]
                result['isadmin'] = val[2]
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': 'User not found.'})

