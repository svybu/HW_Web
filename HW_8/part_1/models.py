from mongoengine import Document, StringField, ListField, ReferenceField

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

class Quote(Document):
    tags = ListField(StringField(), required=True)
    author = StringField(required=True)
    quote = StringField(required=True)
