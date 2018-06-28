from flask import request, jsonify
from modules.appdb import *
from static import checkTokenUser, AUTHIGNORE


class Rating(Resource):
    def get(self):
        vTmp = {}
        jsondata = []
        vTmp['success'] = 0

        _from = request.args.get('_from', "19760101")
        _till = request.args.get('_till', "21000101")
        _persons = request.args.get('_persons', "")
        _sites = request.args.get('_sites', "")
        _groupdate = request.args.get('_groupdate', "day")

        token = request.args.get("token_auth", "")
        admin_id = checkTokenUser(token)
        if admin_id == 0 and AUTHIGNORE is False:
            return jsonify(vTmp)

        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            if _groupdate == 'month':
                groupby = " MONTH(pg.lastScanDate) "
            if _groupdate == 'year':
                groupby = " YEAR(pg.lastScanDate) "

            groupby = " DAY(pg.foundDateTime) "
            if AUTHIGNORE:
                where = "WHERE pg.`lastScanDate` BETWEEN '{}' AND '{}' ".format(_from, _till)
                query = "select ps.*, st.*, sum(ppr.Rank) as rank, DATE_FORMAT(pg.lastScanDate,'%Y-%m-%d')" \
                        " from persons as ps left join personspagerank as ppr " \
                      "ON ppr.`PersonID` = ps.ID left join pages as pg ON pg.ID = ppr.PageID left join sites as st " \
                      "ON st.`ID` = pg.`siteID`" + where + " group by ps.ID, ppr.`PersonID`, st.ID," + groupby
            else:
                """pg.lastScanDate"""
                query = "select ps.*, st.*, sum(ppr.Rank) as rank, DATE_FORMAT(pg.foundDateTime,'%Y-%m-%d') from persons as ps " \
                    "left join personspagerank as ppr ON ppr.`PersonID` = ps.ID left join pages as pg ON pg.ID = ppr.PageID " \
                    "left join sites as st ON st.`ID` = pg.`siteID` " \
                    "where pg.`foundDateTime` BETWEEN '{}' AND '{}' ".format(_from, _till)
                query = query + " AND st.addedBy >= %d " % int(admin_id)
                query = query + " GROUP BY ps.ID, ppr.`PersonID`, st.ID," + groupby

            print(query)
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['person_id'] = val[0]
                vTmp['person_name'] = val[1]
                vTmp['person_addby'] = val[2]
                vTmp['site_id'] = val[3]
                vTmp['site_name'] = val[4]
                vTmp['site_addby'] = val[5]
                vTmp['person_rank'] = int(val[7])
                vTmp['person_rank_date'] = val[8]
                jsondata.append(vTmp)
            return jsonify(jsondata)
        except Exception as e:
            vTmp['exception'] = str(e)
            return jsonify(vTmp)
