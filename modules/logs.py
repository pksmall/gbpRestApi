from flask import request, jsonify
from modules.appdb import *
from static import LIMITPAGE, checkTokenUser, AUTHIGNORE

class Logs(Resource):
    def get(self):
        jsondata = []
        vTmp = {}
        vTmp['success'] = 0

        _sortby = request.args.get("_sortby", "DESC")
        _from = request.args.get('_from', 19760101)
        _till = request.args.get('_till', 21001231)

        token = request.args.get("token_auth", "")
        admin_id = checkTokenUser(token)

        if admin_id == 0 and AUTHIGNORE is False:
            return jsonify(vTmp)

        conn = mysql.connect()
        cursor = conn.cursor()

        try:
            if AUTHIGNORE:
                query = "select *,UNIX_TIMESTAMP(logDate) from log " \
                        "where `logDate` BETWEEN '{}' AND '{}' order by logDate {} LIMIT {}".format(_from, _till, _sortby, LIMITPAGE)
            else:
                query = "select *,UNIX_TIMESTAMP(logDate) from log where adminID >= {} and " \
                        "`logDate` BETWEEN '{}' AND '{}' order by logDate  {} LIMIT {}".format(admin_id, _from, _till, _sortby, LIMITPAGE)

            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['log_id'] = val[0]
                vTmp['log_admin_id'] = val[1]
                vTmp['log_action'] = val[2]
                vTmp['log_date'] = val[4]
                jsondata.append(vTmp)
            return jsonify(jsondata)
        except Exception as e:
            return jsonify(vTmp)
