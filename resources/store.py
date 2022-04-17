from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel 

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",
        type=str,
        required=True,
        help="This field cannot be left blank!")
    
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name {} already exists.".format(name)}, 400
        
        data = Store.parser.parse_args()
        store = StoreModel(data["name"])
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating store'}
        
        return store.json(), 201
        

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}

    