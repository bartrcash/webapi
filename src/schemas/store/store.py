from ma import ma
from models.store.store import StoreModel

# schemas
from schemas.store.item import ItemSchema

class StoreSchema(ma.ModelSchema):
    class Meta:
        model = StoreModel
        include_fk = True

    items = ma.Nested(ItemSchema, many=True)

