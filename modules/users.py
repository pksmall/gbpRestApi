from flask import request, jsonify
from modules.appdb import *
from static import LOGINTIME, checkTokenUser, AUTHIGNORE, insertLog


class Users(Resource):
    def get(self):
        jsondata = []
        vTmp = {}
        vTmp['success'] = 0

        token = request.args.get("token_auth", "")
        admin_id = checkTokenUser(token)

        if admin_id == 0 and AUTHIGNORE is False:
            return jsonify(vTmp)

        conn = mysql.connect()
        cursor = conn.cursor()

        try:
            if AUTHIGNORE:
                query = "select * from users"
            else:
                query = "select * from users where parentID >= %d" % int(admin_id)

            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['user_id'] = val[0]
                vTmp['user_login'] = val[3]
                vTmp['user_email'] = val[5]
                vTmp['user_isadmin'] = val[2]
                vTmp['user_addby'] = val[1]
                vTmp['user_password'] = val[4]
                jsondata.append(vTmp)
            return jsonify(jsondata)
        except Exception as e:
            return jsonify(vTmp)

    def post(self):
        vTmp = {}
        vTmp['success'] = 0
        parent_id = 0

        try:
            if not request.json:
                return jsonify(vTmp)
            else:
                token = request.json['token_auth']

                conn = mysql.connect()
                cursor = conn.cursor()

                query = "select * from users where token = '{}' and isAdmin = 1 and " \
                        "tokenLastAccess > NOW() - INTERVAL {} MINUTE;".format(token, LOGINTIME)
                try:
                    cursor.execute(query)
                    if cursor.rowcount == 1:
                        for userValue in cursor.fetchall():
                            parent_id = userValue[0]
                    else:
                        return jsonify(vTmp)
                except Exception as e:
                    return jsonify(vTmp)
        except Exception as e:
            return jsonify(vTmp)

        try:
            login = request.json['user']
            password = request.json['password']
            email = request.json['email']
            is_admin = request.json['isAdmin']
        except Exception as e:
            return jsonify(vTmp)

        try:
            query = "insert into users (parentID, isAdmin, login, password, email) values('{}','{}'," \
                    "'{}','{}','{}')".format(parent_id, is_admin, login, password, email)
            cursor.execute(query)
            conn.commit()
            vTmp["user_id"] = cursor.lastrowid

            query = "UPDATE users SET token = '{}', tokenLastAccess = now() WHERE ID = {}".format(token, parent_id)
            cursor.execute(query)
            conn.commit()

            insertLog(parent_id, "Создал пользователя {}".format(login))

            vTmp['success'] = 1
            return jsonify(vTmp)
        except Exception as e:
            vTmp['exception'] = str(e)
            return jsonify(vTmp)

    def patch(self):
        vTmp = {}
        vTmp['success'] = 0
        parent_id = 0

        try:
            if not request.json:
                return jsonify(vTmp)
            else:
                token = request.json['token_auth']

                conn = mysql.connect()
                cursor = conn.cursor()

                query = "select * from users where token = '{}' and isAdmin = 1 and " \
                        "tokenLastAccess > NOW() - INTERVAL {} MINUTE;".format(token, LOGINTIME)
                try:
                    cursor.execute(query)
                    if cursor.rowcount == 1:
                        for userValue in cursor.fetchall():
                            parent_id = userValue[0]
                    else:
                        return jsonify(vTmp)
                except Exception as e:
                    return jsonify(vTmp)
        except Exception as e:
            return jsonify(vTmp)

        try:
            user_id = request.json['user_id']
        except:
            return jsonify(vTmp)

        req_json = request.json
        login = ""
        password = ""
        email = ""
        is_admin = ""
        if 'user' in req_json:
            login = req_json['user']
        if 'password' in req_json:
            password = req_json['password']
        if 'email' in req_json:
            email = req_json['email']
        if 'is_admin' in req_json:
            is_admin = req_json['is_admin']

        try:
            query = "SELECT * FROM users WHERE ID = {}".format(user_id)
            cursor.execute(query)
            if cursor.rowcount == 0:
                return jsonify(vTmp)

            query = "UPDATE users SET "
            if 'user' in req_json:
                query = query + "login = '{}' ".format(login)
            if 'password' in req_json:
                if 'user' in req_json:
                    query = query + ", "
                query = query + "password = '{}' ".format(password)
            if 'email' in req_json:
                if 'login' or 'password' in req_json:
                    query = query + ", "
                query = query + "email = '{}' ".format(email)
            if 'is_admin' in req_json:
                if 'login' or 'password' or 'email' in req_json:
                    query = query + ", "
                query = query + "isAdmin = {} ".format(is_admin)
            query = query + "WHERE ID = {} ".format(user_id)
            cursor.execute(query)
            conn.commit()

            query = "UPDATE users SET token = '{}', tokenLastAccess = now() WHERE ID = {}".format(token, parent_id)
            cursor.execute(query)
            conn.commit()

            insertLog(parent_id, "Изменил пользователя {}".format(login))

            vTmp['success'] = 1
            return jsonify(vTmp)
        except Exception as e:
            vTmp['exception'] = str(e)
            return jsonify(vTmp)

    def delete(self):
        vTmp = {}
        vTmp['success'] = 0
        parent_id = 0

        try:
            if not request.json:
                return jsonify(vTmp)
            else:
                req_json = request.json

                if 'token_auth' in req_json:
                    token = request.json['token_auth']
                else:
                    return jsonify(vTmp)

                conn = mysql.connect()
                cursor = conn.cursor()

                query = "select * from users where token = '{}' and isAdmin = 1 and " \
                        "tokenLastAccess > NOW() - INTERVAL {} MINUTE;".format(token, LOGINTIME)
                try:
                    cursor.execute(query)
                    if cursor.rowcount == 1:
                        for userValue in cursor.fetchall():
                            parent_id = userValue[0]
                    else:
                        return jsonify(vTmp)
                except Exception as e:
                    return jsonify(vTmp)
        except Exception as e:
            return jsonify(vTmp)

        if 'user_id' in req_json:
            user_id = request.json['user_id']
        else:
            return jsonify(vTmp)

        try:
            query = "SELECT * FROM users WHERE ID = {}".format(user_id)
            cursor.execute(query)
            if cursor.rowcount >= 1:
                query = "DELETE FROM users WHERE ID = {}".format(user_id)
                cursor.execute(query)
                conn.commit()
            else:
                return jsonify(vTmp)

            query = "UPDATE users SET token = '{}', tokenLastAccess = now() WHERE ID = {}".format(token, parent_id)
            cursor.execute(query)
            conn.commit()

            insertLog(parent_id, "Удалил пользователя с id {}".format(user_id))

            vTmp['success'] = 1
            return jsonify(vTmp)
        except Exception as e:
            vTmp['exception'] = str(e)
            return jsonify(vTmp)


class UsersByID(Resource):
    def get(self, user_id):
        vTmp = {}
        vTmp['success'] = 0

        token = request.args.get("token_auth", "")
        admin_id = checkTokenUser(token)

        if admin_id == 0 and AUTHIGNORE is False:
            return jsonify(vTmp)

        conn = mysql.connect()
        cursor = conn.cursor()

        try:
            if AUTHIGNORE:
                query = "select * from users where ID = %d " % int(user_id)
            else:
                if int(user_id) == int(admin_id):
                    query = "select * from users where ID = %d " % int(user_id)
                else:
                    query = "select * from users where ID = {} and parentID >= {}".format(user_id, admin_id)
            try:
                cursor.execute(query)
                for val in cursor.fetchall():
                    result = {}
                    result['user_id'] = val[0]
                    result['user_login'] = val[3]
                    result['user_email'] = val[5]
                    result['user_isadmin'] = val[2]
                    result['user_addby'] = val[1]
                    result['user_password'] = val[4]
                return jsonify(result)
            except:
                return jsonify(vTmp)
        except:
            return jsonify(vTmp)

