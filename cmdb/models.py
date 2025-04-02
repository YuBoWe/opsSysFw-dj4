from mongoengine import (
     Document, StringField, IntField, EmbeddedDocument, ListField, BooleanField, EmbeddedDocumentField,
     DynamicDocument
)


class CiTypeField(EmbeddedDocument):
     meta = {'collection': 'citypes', 'app_label': 'cmdb', 'model_name': 'citype'}
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


class Ci(DynamicDocument):
    # 字段取决于CiType中某一种类型在fields中定义的字段，可以说几乎每种类型的字段都不一样
    meta = {'collection': 'cis', 'app_label': 'cmdb', 'model_name': 'citype'}
