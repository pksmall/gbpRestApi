from flask import request, jsonify
from modules.appdb import *
from static import  LOGINTIME


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
                    return jsonify(vTmp)
        except Exception as e:
            return jsonify(vTmp)

        try:
            name = request.json['name']
        except Exception as e:
            return jsonify(vTmp)

        try:
            query = "insert into persons (addedBy, name) values('{}','{}')".format(parent_id, name)
            print(query)
            cursor.execute(query)
            conn.commit()
            vTmp["person_id"] = cursor.lastrowid

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
            name = request.json['name']
            person_id = request.json['person_id']
        except:
            return jsonify(vTmp)

        try:
            query = "SELECT * FROM persons WHERE ID = {}".format(person_id)
            cursor.execute(query)
            if cursor.rowcount == 0:
                return jsonify(vTmp)

            query = "UPDATE persons SET name = '{}' WHERE ID = {} ".format(name, person_id)
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

        if 'person_id' in req_json:
            person_id = request.json['person_id']
        else:
            return jsonify(vTmp)

        try:
            query = "SELECT * FROM persons WHERE ID = {}".format(person_id)
            cursor.execute(query)
            if cursor.rowcount >= 1:
                query = "DELETE FROM persons WHERE ID = {}".format(person_id)
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


class PersonsKeywords(Resource):
    def post(self):
        vTmp = {}
        vTmp['success'] = 0
        parent_id = 0
        """ {"Ким Чин Ыну", "Ким Чин Ына", "Ким Чин Ыном","Ким Чин Ынамом"  } """

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
            person_id = request.json['person_id']
            keywords = request.json['keywords']
        except Exception as e:
            return jsonify(vTmp)

        try:
            keyIDs = []
            for key in keywords:
                query = "insert into keywords (personID, name) values('{}','{}')".format(person_id, keywords[key])
                print(query)
                cursor.execute(query)
                conn.commit()
                keyIDs.append(cursor.lastrowid)
            vTmp["keywords_id"] = keyIDs

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
            name = request.json['name']
            keyword_id = request.json['keyword_id']
        except:
            return jsonify(vTmp)

        try:
            query = "SELECT * FROM keywords WHERE ID = {}".format(keyword_id)
            cursor.execute(query)
            if cursor.rowcount == 0:
                return jsonify(vTmp)

            query = "UPDATE keywords SET name = '{}' WHERE ID = {} ".format(name, keyword_id)
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

        if 'keyword_id' in req_json:
            keyword_id = request.json['keyword_id']
        else:
            return jsonify(vTmp)

        try:
            query = "SELECT * FROM keywords WHERE ID = {}".format(keyword_id)
            cursor.execute(query)
            if cursor.rowcount >= 1:
                query = "DELETE FROM keywords WHERE ID = {}".format(keyword_id)
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
        except:
            return jsonify({'message': 'Person not found.', "success": 0})


class PersonsRank(Resource):
    def get(self):
        vTmp = {}
        jsondata = []
        vTmp['success'] = 0

        conn = mysql.connect()
        cursor = conn.cursor()
        groupby = request.args.get("groupby", "")
        siteid = int(request.args.get("siteID", 0))

        if groupby == 'siteID':
            if siteid > 0:
               where = " WHERE st.ID = %d" % int(siteid)
            else:
                where = ""
            query = "select ps.*, st.*, sum(ppr.Rank) as rank from persons as ps left join personspagerank as ppr " \
                  "ON ppr.`PersonID` = ps.ID left join pages as pg ON pg.ID = ppr.PageID left join sites as st " \
                  "ON st.`ID` = pg.`siteID`" + where + " group by ps.ID, ppr.`PersonID`, st.ID"
        else:
            query = "select * from personspagerank;"

        cursor.execute(query)
        for val in cursor.fetchall():
            vTmp = {}
            if groupby:
                vTmp['id'] = val[0]
                vTmp['person_name'] = val[1]
                vTmp['person_addby'] = val[2]
                vTmp['site_id'] = val[3]
                vTmp['site_name'] = val[4]
                vTmp['site_addby'] = val[5]
                vTmp['person_rank'] = str(val[7])
            else:
                vTmp['id'] = val[3]
                vTmp['personid'] = val[0]
                vTmp['pageid'] = val[1]
                vTmp['rank'] = val[2]
            jsondata.append(vTmp)
        return jsonify(jsondata)


class PersonsRankById(Resource):
    def get(self, persons_id):
        vTmp = {}
        jsondata = []
        vTmp['success'] = 0

        groupby = request.args.get("groupby", "")
        siteid = int(request.args.get("siteID", 0))
        conn = mysql.connect()
        cursor = conn.cursor()
        if groupby == 'siteID':
            where = " WHERE "
            if siteid > 0:
                where = where + "st.ID = %d AND " % int(siteid)

            where = where + " ppr.PersonID = %d" % int(persons_id)
            query = "select ps.*, st.*, sum(ppr.Rank) as rank from persons as ps left join personspagerank as ppr " \
                  "ON ppr.`PersonID` = ps.ID left join pages as pg ON pg.ID = ppr.PageID left join sites as st " \
                  "ON st.`ID` = pg.`siteID`" + where + " group by ps.ID, ppr.`PersonID`, st.ID"
        else:
            query = "select * from personspagerank where PersonID =%d " % int(persons_id)

        print(query)
        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                if groupby:
                    vTmp['id'] = val[0]
                    vTmp['person_name'] = val[1]
                    vTmp['person_addby'] = val[2]
                    vTmp['site_id'] = val[3]
                    vTmp['site_name'] = val[4]
                    vTmp['site_addby'] = val[5]
                    vTmp['person_rank'] = str(val[7])
                else:
                    vTmp['id'] = val[3]
                    vTmp['personid'] = val[0]
                    vTmp['pageid'] = val[1]
                    vTmp['rank'] = val[2]
                jsondata.append(vTmp)
            return jsonify(jsondata)
        except Exception as e:
            return jsonify({'message': 'Person not found.' + str(e), "success": 0})


class PersonsRankDate(Resource):
    def get(self):
        vTmp = {}
        jsondata = []
        vTmp['success'] = 0

        groupby = request.args.get("groupby", "")
        siteid = int(request.args.get("siteID", 0))
        _from = request.args.get('_from', 1)
        _till = request.args.get('_till', 1)
        conn = mysql.connect()
        cursor = conn.cursor()
        if groupby == 'siteID':
            where = " WHERE "
            if siteid > 0:
                where = where + "st.ID = %d AND " % int(siteid)
            where = where + " pg.`lastScanDate` BETWEEN '{}' AND '{}' ".format(_from, _till)
            query = "select ps.*, st.*, sum(ppr.Rank) as rank from persons as ps left join personspagerank as ppr " \
                  "ON ppr.`PersonID` = ps.ID left join pages as pg ON pg.ID = ppr.PageID left join sites as st " \
                  "ON st.`ID` = pg.`siteID`" + where + " group by ps.ID, ppr.`PersonID`, st.ID"
        else:
           query = "select * from persons as ps left join personspagerank as ppr ON ppr.`PersonID` = ps.ID left join pages \
                    as pg ON pg.ID = ppr.PageID left join sites as st ON st.`ID` = pg.`siteID` \
                where pg.`lastScanDate` BETWEEN '{}' AND '{}'".format(_from, _till)
        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                if groupby:
                    vTmp['id'] = val[0]
                    vTmp['person_name'] = val[1]
                    vTmp['person_addby'] = val[2]
                    vTmp['site_id'] = val[3]
                    vTmp['site_name'] = val[4]
                    vTmp['site_addby'] = val[5]
                    vTmp['person_rank'] = str(val[7])
                else:
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
            return jsonify({'message': 'data not found.', "success": 0})


class PersonsRankDateById(Resource):
    def get(self, persons_id):
        vTmp = {}
        jsondata = []
        vTmp['success'] = 0

        groupby = request.args.get("groupby", "")
        siteid = int(request.args.get("siteID", 0))
        _from = request.args.get('_from', 1)
        _till = request.args.get('_till', 1)
        conn = mysql.connect()
        cursor = conn.cursor()
        if groupby == 'siteID':
            where = " WHERE "
            if siteid > 0:
                where = where + "st.ID = %d AND " % int(siteid)
            where = where + " pg.`lastScanDate` BETWEEN '{}' AND '{}' AND ps.ID = {}".format(_from, _till, persons_id)
            query = "select ps.*, st.*, sum(ppr.Rank) as rank from persons as ps left join personspagerank as ppr " \
                  "ON ppr.`PersonID` = ps.ID left join pages as pg ON pg.ID = ppr.PageID left join sites as st " \
                  "ON st.`ID` = pg.`siteID`" + where + " group by ps.ID, ppr.`PersonID`, st.ID"
        else:
            query = "select * from persons as ps left join personspagerank as ppr ON ppr.`PersonID` = ps.ID left join pages \
                    as pg ON pg.ID = ppr.PageID left join sites as st ON st.`ID` = pg.`siteID` \
                where  pg.`lastScanDate` BETWEEN '{}' AND '{}' AND ps.ID = {}".format(_from, _till, persons_id)
        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                if groupby:
                    vTmp['id'] = val[0]
                    vTmp['person_name'] = val[1]
                    vTmp['person_addby'] = val[2]
                    vTmp['site_id'] = val[3]
                    vTmp['site_name'] = val[4]
                    vTmp['site_addby'] = val[5]
                    vTmp['person_rank'] = str(val[7])
                else:
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
            return jsonify({'message': 'data not found.', "success": 0})
