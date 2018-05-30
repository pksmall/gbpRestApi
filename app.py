from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flaskext.mysql import MySQL

mysql = MySQL()

app = Flask(__name__)
api = Api(app)

# MySQL configurations
app.config['JSON_AS_ASCII'] = False
app.config['MYSQL_DATABASE_USER'] = 'apiuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PassToUserApi'
app.config['MYSQL_DATABASE_DB'] = 'searchandratewords'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class Users(Resource):
    def get(self):
        jsondata = []
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from users"
        cursor.execute(query)
        for val in cursor.fetchall():
            vTmp = {}
            vTmp['id'] = val[0]
            vTmp['login'] = val[3]
            vTmp['email'] = val[5]
            vTmp['isadmin'] = val[2]
            jsondata.append(vTmp)
        return jsonify(jsondata)

    def post(self):
        conn = mysql.connect()
        cursor = conn.cursor(buffered=True)

        print(request.json)
        login = request.json['login']
        password = request.json['password']
        email = request.json['email']

        if request.json['isAdmin']:
            is_admin = request.json['isAdmin']
        else:
            is_admin = 0
        if request.json['parentID']:
            parent_id = request.json['parentID']
        else:
            parent_id = 0
        query = "insert into employees values(null,'{0}','{1}', \
                            '{2}','{3}','{4}')".format(parent_id, is_admin, login, password, email)
        cursor.execute(query)
        conn.commit()
        return {'status': 'success'}


class UsersByID(Resource):
    def get(self, user_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from users where ID = %d " % int(user_id)

        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                result = {}
                result['id'] = val[0]
                result['login'] = val[3]
                result['email'] = val[5]
                result['isadmin'] = val[2]
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': 'User not found.'})


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
        conn = mysql.connect()
        query = "select * from personspagerank where ID =%d " % int(persons_id)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            for val in cursor.fetchall():
                vTmp = {}
                vTmp['id'] = val[3]
                vTmp['personid'] = val[0]
                vTmp['pageid'] = val[1]
                vTmp['rank'] = val[2]
            return jsonify(vTmp)
        except Exception as e:
            return jsonify({'error': 'Person not found.' + str(e)})


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
            vTmp['siteDescription'] = val[2]
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
                result['siteDescription'] = val[1]
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': 'Site not found.' + str(e)})


api.add_resource(Users, '/v1/users')
api.add_resource(UsersByID, '/v1/users/<user_id>')
api.add_resource(Persons, '/v1/persons')
api.add_resource(PersonsById, '/v1/persons/<persons_id>')
api.add_resource(PersonsRank, '/v1/persons/rank')
api.add_resource(PersonsRankById, '/v1/persons/rank/<persons_id>')
api.add_resource(Sites, '/v1/sites')
api.add_resource(SiteByID, '/v1/sites/<site_id>')

if __name__ == '__main__':
    app.run(debug=True)
