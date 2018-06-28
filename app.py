from static import *
from modules.users import *
from modules.persons import *
from modules.sites import *
from modules.pages import *
from modules.renew import *
from modules.rating import *
from modules.auth import *

class Info(Resource):
    def get(self):
        return jsonify(API_DESC)


@app.errorhandler(404)
def err404(self):
    return jsonify(ERR404)


@app.errorhandler(500)
def err500(self):
    return jsonify(ERR500)


api.add_resource(Info, '/v1')
api.add_resource(Users, '/v1/users')
api.add_resource(UsersByID, '/v1/users/<user_id>')
api.add_resource(Persons, '/v1/persons')
api.add_resource(PersonsKeywords, '/v1/persons/keywords')
api.add_resource(PersonsById, '/v1/persons/<persons_id>')
api.add_resource(PersonsRank, '/v1/persons/rank')
api.add_resource(PersonsRankById, '/v1/persons/rank/<persons_id>')
api.add_resource(PersonsRankDate, '/v1/persons/rank/date')
api.add_resource(PersonsRankDateById, '/v1/persons/rank/<persons_id>/date')
api.add_resource(Sites, '/v1/sites')
api.add_resource(SiteByID, '/v1/sites/<site_id>')
api.add_resource(Auth, '/v1/auth')
api.add_resource(Pages, '/v1/pages')
api.add_resource(PagesByID, '/v1/pages/<page_id>')
api.add_resource(Renew, '/v1/renew')
api.add_resource(Rating, '/v1/rating')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
