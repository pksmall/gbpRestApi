from flask import request, jsonify
from modules.appdb import *
from static import LOGINTIME, checkTokenUser, AUTHIGNORE, LIMITPAGE, insertLog


class Pages(Resource):
    def get(self):
        jsondata = []
        vTmp = {}
        vTmp['success'] = 0

        token = request.args.get("token_auth", "")
        admin_id = checkTokenUser(token)

        if admin_id == 0 and AUTHIGNORE is False:
            return jsonify(vTmp)

        _page = request.args.get('_page', 0)
        _siteID = int(request.args.get('siteID', 0))

        conn = mysql.connect()
        cursor = conn.cursor()

        try:
            where = " WHERE "
            if _siteID > 0:
                where = where + " st.ID = %d " % int(_siteID)
            else:
                where = ""

            if AUTHIGNORE:
                query = "select *,UNIX_TIMESTAMP(foundDatetime),UNIX_TIMESTAMP(lastScanDate) from pages " \
                        "" + where + " ORDER BY ID LIMIT {} OFFSET {}".format(LIMITPAGE, _page)
            else:
                if where != "":
                    where = where + " AND st.addedBy >= {}".format(admin_id)
                else:
                    where = "WHERE st.addedBy >= {}".format(admin_id)
                query = "select *,UNIX_TIMESTAMP(foundDatetime),UNIX_TIMESTAMP(lastScanDate) from pages  as pg " \
                        "left join sites as st ON st.`ID` = pg.`siteID` " \
                        "" + where + " ORDER BY pg.ID LIMIT {} OFFSET {} ".format(LIMITPAGE, _page)
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['page_id'] = val[0]
                vTmp['page_url'] = val[1]
                vTmp['page_site_id'] = val[2]
                vTmp['page_found_date_str'] = val[3]
                vTmp['page_last_scan_date_str'] = val[4]
                if AUTHIGNORE:
                    vTmp['page_found_date'] = val[5]
                    vTmp['page_last_scan_date'] = val[6]
                else:
                    vTmp['page_found_date'] = val[9]
                    vTmp['page_last_scan_date'] = val[10]
                jsondata.append(vTmp)
            return jsonify(jsondata)
        except Exception as e:
            vTmp['exception'] = str(e)
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
            page_url = request.json['page_url']
            page_site_id = request.json['page_site_id']
        except Exception as e:
            return jsonify(vTmp)

        req_json = request.json
        if 'page_found_date' in req_json:
            page_fd = request.json['page_found_date']
        else:
            page_fd = "Null"
        if 'page_last_scan_date' in req_json:
            page_lsd = request.json['page_last_scan_date']
        else:
            page_lsd = "Null"

        try:
            query = "insert into pages (URL, siteID, foundDateTime, lastScanDate) values('{}','{}'," \
                    "{},{})".format(page_url, page_site_id, page_fd, page_lsd)
            cursor.execute(query)
            conn.commit()
            vTmp["page_id"] = cursor.lastrowid

            query = "UPDATE users SET token = '{}', tokenLastAccess = now() WHERE ID = {}".format(token, parent_id)
            cursor.execute(query)
            conn.commit()

            insertLog(parent_id, "Добавлена страница c url {}".format(page_url))

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
            vTmp['exception'] = str(e)
            return jsonify(vTmp)

        try:
            page_id = request.json['page_id']
        except Exception as e:
            return jsonify(vTmp)

        req_json = request.json
        if 'page_url' in req_json:
            page_url = req_json['page_url']
        if 'page_found_date' in req_json:
            page_fd = req_json['page_found_date']
        if 'page_last_scan_date' in req_json:
            page_lsd = req_json['page_last_scan_date']
        if 'page_site_id' in req_json:
            page_site_id = req_json['page_site_id']

        try:
            query = "SELECT * FROM pages WHERE ID = {}".format(page_id)
            cursor.execute(query)
            if cursor.rowcount == 0:
                return jsonify(vTmp)

            query = "UPDATE pages SET "
            if 'page_url' in req_json:
                query = query + "URL = '{}' ".format(page_url)
            if 'page_found_date' in req_json:
                if 'page_url' in req_json:
                    query = query + ", "
                query = query + "foundDateTime = {} ".format(page_fd)
            if 'page_last_scan_date' in req_json:
                if 'page_url' or 'page_found_date' in req_json:
                    query = query + ", "
                query = query + "lastScanDate = {} ".format(page_lsd)
            if 'page_site_id' in req_json:
                if 'page_url' or 'page_found_date' or 'page_last_scan_date' in req_json:
                    query = query + ", "
                query = query + "siteID = {} ".format(page_site_id)
            query = query + "WHERE ID = {} ".format(page_id)
            cursor.execute(query)
            conn.commit()

            query = "UPDATE users SET token = '{}', tokenLastAccess = now() WHERE ID = {}".format(token, parent_id)
            cursor.execute(query)
            conn.commit()

            insertLog(parent_id, "Изменил страницу id {}".format(page_id))

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

        if 'page_id' in req_json:
            page_id = request.json['page_id']
        else:
            return jsonify(vTmp)

        try:
            query = "SELECT * FROM pages WHERE ID = {}".format(page_id)
            cursor.execute(query)
            if cursor.rowcount >= 1:
                query = "DELETE FROM pages WHERE ID = {}".format(page_id)
                cursor.execute(query)
                conn.commit()
            else:
                return jsonify(vTmp)

            query = "UPDATE users SET token = '{}', tokenLastAccess = now() WHERE ID = {}".format(token, parent_id)
            cursor.execute(query)
            conn.commit()

            insertLog(parent_id, "Удалил страницу id {}".format(page_id))

            vTmp['success'] = 1
            return jsonify(vTmp)
        except Exception as e:
            vTmp['exception'] = str(e)
            return jsonify(vTmp)


class PagesByID(Resource):
    def get(self, page_id):
        vTmp = {}
        vTmp['success'] = 0

        token = request.args.get("token_auth", "")
        admin_id = checkTokenUser(token)

        if admin_id == 0 and AUTHIGNORE is False:
            return jsonify(vTmp)

        conn = mysql.connect()
        cursor = conn.cursor()

        try:
            where = " WHERE "

            if AUTHIGNORE:
                query = "select *,UNIX_TIMESTAMP(foundDatetime),UNIX_TIMESTAMP(lastScanDate) from pages "\
                        + where + " ID = %d" % int(page_id)
            else:
                where = "WHERE st.addedBy >= {} AND pg.ID = {} ".format(admin_id, page_id)
                query = "select *,UNIX_TIMESTAMP(foundDatetime),UNIX_TIMESTAMP(lastScanDate) from pages  as pg " \
                        "left join sites as st ON st.`ID` = pg.`siteID` " \
                        "" + where

            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['page_id'] = val[0]
                vTmp['page_url'] = val[1]
                vTmp['page_site_id'] = val[2]
                vTmp['page_found_date_str'] = val[3]
                vTmp['page_last_scan_date_str'] = val[4]
                if AUTHIGNORE:
                    vTmp['page_found_date'] = val[5]
                    vTmp['page_last_scan_date'] = val[6]
                else:
                    vTmp['page_found_date'] = val[9]
                    vTmp['page_last_scan_date'] = val[10]
            return jsonify(vTmp)
        except:
            return jsonify(vTmp)
