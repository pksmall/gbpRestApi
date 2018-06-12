from flask import request, jsonify
from modules.appdb import *
from static import  LOGINTIME

class Sites(Resource):
    def get(self):
        jsondata = []
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from sites;"
        cursor.execute(query)
        for val in cursor.fetchall():
            vTmp = {}
            vTmp['id'] = val[0]
            vTmp['addby'] = val[2]
            vTmp['name'] = val[1]
            vTmp['siteDescription'] = val[3]
            jsondata.append(vTmp)
        return jsonify(jsondata)

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

                query = "select * from users where token = '{}' and " \
                        "tokenLastAccess > NOW() - INTERVAL {} MINUTE;".format(token, LOGINTIME)
                print(query)
                try:
                    cursor.execute(query)
                    if cursor.rowcount == 1:
                        for userValue in cursor.fetchall():
                            parent_id = userValue[0]
                    else:
                        return jsonify(vTmp)
                except Exception as e:
                    vTmp['exception'] = str(e)
                    return jsonify(vTmp)
        except Exception as e:
            vTmp['exception'] = str(e)
            return jsonify(vTmp)

        try:
            name = request.json['name']
            description = request.json['description']
            pageURL = request.json['pageURL']
        except Exception as e:
            vTmp['exception'] = str(e)
            return jsonify(vTmp)

        try:
            query = "insert into sites (addedBy, name, siteDescription) values({}, '{}', '{}')".format(parent_id, name, description)
            print(query)
            cursor.execute(query)
            conn.commit()
            vTmp["site_id"] = cursor.lastrowid

            query = "insert into pages (URL, siteID, foundDateTime) values({}, '{}',  now())".format(pageURL, vTmp['site_id'])
            cursor.execute(query)
            conn.commit()

            query = "UPDATE users SET token = '{}', tokenLastAccess = now() WHERE ID = {}".format(token, parent_id)
            cursor.execute(query)
            conn.commit()

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

                query = "select * from users where token = '{}' and " \
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
            site_id = request.json['site_id']
        except:
            return jsonify(vTmp)

        req_json = request.json
        name = ""
        description = ""
        if 'name' in req_json:
            name = req_json['name']
        if 'description' in req_json:
            description = req_json['description']

        try:
            query = "SELECT * FROM sites WHERE ID = {}".format(site_id)
            cursor.execute(query)
            if cursor.rowcount == 0:
                return jsonify(vTmp)

            query = "UPDATE sites SET "
            if 'name' in req_json:
                query = query + "name = '{}' ".format(name)
            if 'description' in req_json:
                if 'name' in req_json:
                    query = query + ", "
                query = query + "siteDescription= '{}' ".format(description)
            query = query + "WHERE ID = {} ".format(site_id)
            print(query)
            cursor.execute(query)
            conn.commit()

            query = "UPDATE users SET token = '{}', tokenLastAccess = now() WHERE ID = {}".format(token, parent_id)
            cursor.execute(query)
            conn.commit()

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

                query = "select * from users where token = '{}' and " \
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
            site_id = request.json['site_id']
        except:
            return jsonify(vTmp)

        try:
            query = "SELECT * FROM sites WHERE ID = {}".format(site_id)
            cursor.execute(query)
            if cursor.rowcount >= 1:
                query = "DELETE FROM sites WHERE ID = {}".format(site_id)
                cursor.execute(query)
                conn.commit()
            else:
                return jsonify(vTmp)

            query = "UPDATE users SET token = '{}', tokenLastAccess = now() WHERE ID = {}".format(token, parent_id)
            cursor.execute(query)
            conn.commit()

            vTmp['success'] = 1
            return jsonify(vTmp)
        except Exception as e:
            vTmp['exception'] = str(e)
            return jsonify(vTmp)


class SiteByID(Resource):
    def get(self, site_id):
        conn = mysql.connect()
        query = "select * from sites where ID =%d " % int(site_id)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                result = {}
                result['id'] = val[0]
                result['addby'] = val[2]
                result['name'] = val[1]
                result['siteDescription'] = val[3]
            return jsonify(result)
        except Exception as e:
            return jsonify({'message': 'Site not found.' + str(e)})
