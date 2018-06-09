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
                kTmp = {}
                kTmp['id'] = 0
                kTmp['name'] = val[1]
                result['keywords'].append(kTmp)
                for (kid, kname) in cursor.fetchall():
                    kTmp = {}
                    kTmp['id'] = kid
                    kTmp['name'] = kname
                    result['keywords'].append(kTmp)
            return jsonify(result)
        except Exception as e:
            return jsonify({'message': 'Person not found.' + str(e)})


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
            return jsonify({'message': 'Person not found.' + str(e)})


class PersonsRankDate(Resource):
    def get(self):
        jsondata = []
        conn = mysql.connect()

        _from = request.args.get('_from', 1)
        _till = request.args.get('_till', 1)

        query = "select * from persons as ps left join personspagerank as ppr ON ppr.`PersonID` = ps.ID left join pages \
                    as pg ON pg.ID = ppr.PageID left join sites as st ON st.`ID` = pg.`siteID` \
                where DATE(pg.`lastScanDate`) >=  '{}' AND DATE(pg.lastScanDAte) <= '{}'".format(_from, _till)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['person_id'] = val[0]
                vTmp['person_name'] = val[1]
                vTmp['person_addby'] = val[2]
                vTmp['page_id'] = val[4]
                vTmp['rank'] = val[5]
                vTmp['person_page_id'] = val[7]
                vTmp['page_url'] = val[8]
                vTmp['page_site_id'] = val[9]
                vTmp['site_found_date'] = val[10]
                vTmp['site_last_scan_date'] = val[11]
                vTmp['site_id'] = val[12]
                vTmp['site_name'] = val[13]
                vTmp['site_addby'] = val[14]
                vTmp['site_description'] = val[15]
                jsondata.append(vTmp)
            return jsonify(jsondata)
        except Exception as e:
            return jsonify({'message': 'data not found.' + str(e)})


class PersonsRankDateById(Resource):
    def get(self, persons_id):
        jsondata = []
        conn = mysql.connect()

        _from = request.args.get('_from', 1)
        _till = request.args.get('_till', 1)

        query = "select * from persons as ps left join personspagerank as ppr ON ppr.`PersonID` = ps.ID left join pages \
                    as pg ON pg.ID = ppr.PageID left join sites as st ON st.`ID` = pg.`siteID` \
                where DATE(pg.`lastScanDate`) >=  '{}' AND DATE(pg.lastScanDAte) <= '{}' and ps.ID = {}".format(_from, _till, persons_id)
        cursor = conn.cursor()

        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['person_id'] = val[0]
                vTmp['person_name'] = val[1]
                vTmp['person_addby'] = val[2]
                vTmp['page_id'] = val[4]
                vTmp['rank'] = val[5]
                vTmp['person_page_id'] = val[7]
                vTmp['page_url'] = val[8]
                vTmp['page_site_id'] = val[9]
                vTmp['site_found_date'] = val[10]
                vTmp['site_last_scan_date'] = val[11]
                vTmp['site_id'] = val[12]
                vTmp['site_name'] = val[13]
                vTmp['site_addby'] = val[14]
                vTmp['site_description'] = val[15]
                jsondata.append(vTmp)
            return jsonify(jsondata)
        except Exception as e:
            return jsonify({'message': 'data not found.' + str(e)})
