from flask import Blueprint
from flask_restful import Api
from resources.store.store import Store, StoreList, StoreCreation, StoreByUser
from resources.store.item import Item, ItemCreation

# Create bluepirnt
store_app = Blueprint('store', __name__)
api = Api(store_app)


# Add resources
# Stores
api.add_resource(Store, '/<int:id>')
api.add_resource(StoreList, '/all')
api.add_resource(StoreByUser, '/ownstores')
api.add_resource(StoreCreation, '/creation')

# Items
api.add_resource(Item, '/item/<int:id>')
api.add_resource(ItemCreation, '/item')


