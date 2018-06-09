from flask import request, jsonify
from uuid import uuid4
from modules.appdb import *


class Auth(Resource):
    def getToken(self):
        token = uuid4()
        return token

    def post(self):
        vTmp = {}
        vTmp['success'] = 0

        try:
            if not request.json:
                return jsonify(vTmp)
            else:
                login = request.json['user']
                password = request.json['password']
        except:
            return jsonify(vTmp)

        conn = mysql.connect()
        cursor = conn.cursor()

        query = "select * from users where login = '{}' and password = '{}' and \
                    (token is NULL or tokenLastAccess < NOW() - INTERVAL 60 MINUTE);".format(login, password)
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
            return jsonify(vTmp)
        except Exception as e:
            return jsonify({'message': 'data not found. ' + str(e)})

    def patch(self):
        vTmp = {}
        vTmp['success'] = 0

        try:
            if not request.json:
                return jsonify(vTmp)
            else:
                token = request.json['token_auth']
        except:
            return jsonify(vTmp)

        conn = mysql.connect()
        cursor = conn.cursor()

        query = "select * from users where token = '{}' and tokenLastAccess > NOW() - INTERVAL 60 MINUTE;".format(token)
        cursor.execute(query)
        try:
            if cursor.rowcount == 1:
                for userValue in cursor.fetchall():
                    userId = userValue[0]
                vTmp['success'] = 1
                query = "UPDATE users SET tokenLastAccess = now() WHERE ID = {}".format(userId)
                cursor.execute(query)
                conn.commit()
            return jsonify(vTmp)
        except Exception as e:
            return jsonify({'message': 'data not found. ' + str(e)})
