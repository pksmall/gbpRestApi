from flask import request, jsonify
from uuid import uuid4
from modules.appdb import *
from static import  LOGINTIME


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

        query = "select * from users where lower(login) = '{}' and password = '{}' and \
                    (token is NULL or tokenLastAccess < NOW() - INTERVAL {} MINUTE);".format(login, password, LOGINTIME)
        cursor.execute(query)
        try:
            if cursor.rowcount == 1:
                for userValue in cursor.fetchall():
                    userId = userValue[0]
                vTmp['user_id'] = userId
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

        query = "select * from users where token = '{}' and \
                tokenLastAccess > NOW() - INTERVAL {} MINUTE;".format(token, LOGINTIME)
        try:
            cursor.execute(query)
            if cursor.rowcount == 1:
                for userValue in cursor.fetchall():
                    userId = userValue[0]
                vTmp['user_id'] = userId
                vTmp['success'] = 1
                query = "UPDATE users SET tokenLastAccess = now() WHERE ID = {}".format(userId)
                cursor.execute(query)
                conn.commit()
            return jsonify(vTmp)
        except Exception as e:
            return jsonify({'message': 'data not found. ' + str(e)})

    def delete(self):
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

        query = "select * from users where token = '{}'".format(token)
        try:
            cursor.execute(query)
            if cursor.rowcount == 1:
                for userValue in cursor.fetchall():
                    userId = userValue[0]
                vTmp['success'] = 1
                query = "UPDATE users SET token = NULL, tokenCreatedDate = NULL, \
                    tokenLastAccess = NULL WHERE ID = {}".format(userId)
                cursor.execute(query)
                conn.commit()
            return jsonify(vTmp)
        except Exception as e:
            return jsonify({'message': 'data not found. ' + str(e)})
