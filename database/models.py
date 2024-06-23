from mongoengine import Document, EmbeddedDocument, fields, connect

connect(host='mongodb://root:example@node:27777', db='15min')

class Categories(EmbeddedDocument):
    main = fields.StringField(required=True)
    sub = fields.StringField(required=True)

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
    categories = fields.EmbeddedDocumentField(Categories, required=True)
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