from mongoengine import (
     Document, StringField, IntField, EmbeddedDocument, ListField, BooleanField, EmbeddedDocumentField
)


class CiTypeField(EmbeddedDocument):
     meta = {'collection': 'citypes'}
     name = StringField()
     label = StringField()
     type = StringField()
     required = BooleanField(default=False)


class CiType(Document):
     meta = {'collection': 'citypes'}
     name = StringField(required=True, max_length=32)
     label = StringField()
     version = IntField()
     fields = ListField(EmbeddedDocumentField(CiTypeField))
