from mongoengine import Document, StringField, EmailField, BooleanField

class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    message_sent = BooleanField(default=False)
    additional_info = StringField()
