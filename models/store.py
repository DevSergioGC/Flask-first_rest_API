from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic") 
    #? "lazy=dynamic" fetch the items when we tell it to do it, not before
    
    #? "cascade" means to delete all the reference data related to the model we are deleting
    #? specifies that when a store is deleted, all of its related items should also be deleted.