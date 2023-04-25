from mongoengine import Document, StringField, ListField, ReferenceField

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

    def to_dict(self):
        return {
            'fullname': self.fullname,
            'born_date': self.born_date,
            'born_location': self.born_location
        }

    def __str__(self):
        return f"{self.fullname} was born on {self.born_date} in {self.born_location}"

class Quote(Document):
    tags = ListField(StringField(), required=True)
    author = StringField(required=True)
    quote = StringField(required=True)
