from flask import request, jsonify
from modules.appdb import *


class Persons(Resource):
    def get(self):
        jsondata = []
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from persons;"
        cursor.execute(query)
        for val in cursor.fetchall():
            vTmp = {}
            vTmp['id'] = val[0]
            vTmp['name'] = val[1]
            vTmp['addby'] = val[2]
            jsondata.append(vTmp)
        return jsonify(jsondata)


class PersonsById(Resource):
    def get(self, persons_id):
        conn = mysql.connect()
        query = "select * from persons where ID =%d " % int(persons_id)
        key_qry = "select id,name from keywords where personID =%d " % int(persons_id)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                result = {}
                result['keywords'] = []
                result['id'] = val[0]
                result['name'] = val[1]
                result['addby'] = val[2]
                cursor.execute(key_qry)
                for (kid, kname) in cursor.fetchall():
                    kTmp = {}
                    kTmp['id'] = kid
                    kTmp['name'] = kname
                    result['keywords'].append(kTmp)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': 'Person not found.' + str(e)})


class PersonsRank(Resource):
    def get(self):
        jsondata = []
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from personspagerank;"
        cursor.execute(query)
        for val in cursor.fetchall():
            vTmp = {}
            vTmp['id'] = val[3]
            vTmp['personid'] = val[0]
            vTmp['pageid'] = val[1]
            vTmp['rank'] = val[2]
            jsondata.append(vTmp)
        return jsonify(jsondata)


class PersonsRankById(Resource):
    def get(self, persons_id):
        jsondata = []
        conn = mysql.connect()
        query = "select * from personspagerank where PersonID =%d " % int(persons_id)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['id'] = val[3]
                vTmp['personid'] = val[0]
                vTmp['pageid'] = val[1]
                vTmp['rank'] = val[2]
                jsondata.append(vTmp)
            return jsonify(jsondata)
        except Exception as e:
            return jsonify({'error': 'Person not found.' + str(e)})
