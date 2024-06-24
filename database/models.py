from mongoengine import Document, EmbeddedDocument, fields, connect
import os

MONGO_CONNECT = os.environ.get("MONGO_CONNECT", "mongodb://root:example@node:27777/")

connect(host=MONGO_CONNECT, db='15min')


class Category(Document):
    main_category = fields.StringField(required=True)
    sub_category = fields.StringField(required=True)

    meta = {
        'collection': 'category',
        'indexes': [
            {
                'fields': ('main_category', 'sub_category'),
                'unique': True
            }
        ]
    }

class Address(EmbeddedDocument):
    city = fields.StringField(required=True)
    postcode = fields.StringField(required=True)
    street = fields.StringField(required=True)


class Location(EmbeddedDocument):
    latitude = fields.FloatField(required=True)
    longitude = fields.FloatField(required=True)

class ResidentialBuilding(Document):
    location = fields.EmbeddedDocumentField(Location)
    address = fields.EmbeddedDocumentField(Address)
    geometry = fields.ListField(required=True)
    meta = {
        'collection': 'addresses',
        'indexes': [
            {
                'fields': ('location', 'address'),
                'unique': True
            }
        ]
    }

class POI(Document):
    categories = fields.ListField(fields.ReferenceField(Category), required=True)
    name = fields.StringField(required=True)
    address = fields.EmbeddedDocumentField(Address, required=True)
    location = fields.EmbeddedDocumentField(Location, required=True)

    meta = {
        'collection': 'pois',
        'indexes': [
            {
                'fields': ('categories', 'address', 'location'),
                'unique': True
            }
        ]
    }

