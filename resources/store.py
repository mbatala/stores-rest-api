from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import jwt_required

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json() # default status is 200 and it is not necessary to be explicitly put
        return {'message': "Store '{}' not found!".format(name)}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists!".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred while creating the store '{}'.".format(name)}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store '{}' deleted".format(name)}
        else:
            return {"message": "Store '{}' does not exists!".format(name)}, 400


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}
