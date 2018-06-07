from static import *
from modules.users import *
from modules.persons import *
from modules.sites import *

class Info(Resource):
    def get(self):
        return jsonify(API_DESC)


api.add_resource(Info, '/v1')
api.add_resource(Users, '/v1/users')
api.add_resource(UsersByID, '/v1/users/<user_id>')
api.add_resource(Persons, '/v1/persons')
api.add_resource(PersonsById, '/v1/persons/<persons_id>')
api.add_resource(PersonsRank, '/v1/persons/rank')
api.add_resource(PersonsRankById, '/v1/persons/rank/<persons_id>')
api.add_resource(Sites, '/v1/sites')
api.add_resource(SiteByID, '/v1/sites/<site_id>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
