from flask import request, jsonify
from uuid import uuid4
from modules.appdb import *


class Auth(Resource):
    def getToken(self):
        token = uuid4()
        return token

    def post(self):
        vTmp = {}

        login = request.json['user']
        password = request.json['password']

        conn = mysql.connect()
        cursor = conn.cursor()

        query = "select * from users where login = '{}' and password = '{}' and token is NULL;".format(login, password)
        try:
            cursor.execute(query)
            if cursor.rowcount == 1:
                for userValue in cursor.fetchall():
                    userId = userValue[0]
                vTmp['success'] = 1
                vTmp['token_auth'] = self.getToken()
                query = "UPDATE users SET token = '{}', \
                    tokenCreatedDate = now(), tokenLastAccess = now() WHERE ID = {}".format(vTmp['token_auth'], userId)
                cursor.execute(query)
                conn.commit()
            else:
                vTmp['success'] = 0
            return jsonify(vTmp)
        except Exception as e:
            return jsonify({'message': 'data not found. ' + str(e)})

    def patch(self):
        vTmp = {}

        token = request.json['token_auth']

        conn = mysql.connect()
        cursor = conn.cursor()

        query = "select * from users where token = '{}' and tokenLastAccess > NOW() - INTERVAL 60 MINUTE;".format(token)
        print(query)
        cursor.execute(query)
        try:
            if cursor.rowcount == 1:
                for userValue in cursor.fetchall():
                    userId = userValue[0]
                vTmp['success'] = 1
                query = "UPDATE users SET tokenLastAccess = now() WHERE ID = {}".format(userId)
                cursor.execute(query)
                conn.commit()
            else:
                vTmp['success'] = 0
            return jsonify(vTmp)
        except Exception as e:
            return jsonify({'message': 'data not found. ' + str(e)})