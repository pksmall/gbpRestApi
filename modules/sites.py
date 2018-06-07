from flask import request, jsonify
from modules.appdb import *


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
            vTmp['addby'] = val[1]
            vTmp['siteDescription'] = val[3]
            jsondata.append(vTmp)
        return jsonify(jsondata)


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
                result['addby'] = val[1]
                result['siteDescription'] = val[3]
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': 'Site not found.' + str(e)})
