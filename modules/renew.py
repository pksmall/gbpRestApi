from flask import request, jsonify
from modules.appdb import *
from static import LOGINTIME, checkTokenUser, AUTHIGNORE, LIMITPAGE


class Renew(Resource):
    def get(self):
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
                query = "select UNIX_TIMESTAMP(min(pg.foundDateTime)) as minDate, UNIX_TIMESTAMP(max(pg.foundDateTime)) " \
                        "as maxDate from persons as ps left join personspagerank as ppr ON ppr.`PersonID` = ps.ID " \
                        "left join pages as pg ON pg.ID = ppr.PageID " \
                        "left join sites as st ON st.`ID` = pg.`siteID`"
            else:
                where = "WHERE st.addedBy >= {}".format(admin_id)
                query = "select UNIX_TIMESTAMP(min(pg.foundDateTime)) as minDate, UNIX_TIMESTAMP(max(pg.foundDateTime)) " \
                        "as maxDate from persons as ps left join personspagerank as ppr ON ppr.`PersonID` = ps.ID " \
                        "left join pages as pg ON pg.ID = ppr.PageID " \
                        "left join sites as st ON st.`ID` = pg.`siteID`" + where
            print(query)
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['since_date'] = val[0]
                vTmp['till_date'] = val[1]

            if AUTHIGNORE:
                query = "select * from persons"
            else:
                where = "WHERE addedBy >= {}".format(admin_id)
                query = "select * from persons " + where
            cursor.execute(query)
            jsondata = []
            for val in cursor.fetchall():
                pTmp = {}
                pTmp['person_id'] = val[0]
                pTmp['person_name'] = val[1]
                jsondata.append(pTmp)
            vTmp['persons'] = jsondata

            if AUTHIGNORE:
                query = "select * from sites"
            else:
                where = "WHERE addedBy >= {}".format(admin_id)
                query = "select * from sites " + where
            cursor.execute(query)
            jsondata = []
            for val in cursor.fetchall():
                pTmp = {}
                pTmp['site_id'] = val[0]
                pTmp['site_name'] = val[1]
                jsondata.append(pTmp)
            vTmp['sites'] = jsondata

            return jsonify(vTmp)
        except Exception as e:
            vTmp['exception'] = str(e)
            return jsonify(vTmp)
