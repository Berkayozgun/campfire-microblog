from mongoengine import Document, StringField, DateTimeField
from datetime import datetime


class PostModel(Document):
    author = StringField(required=True)
    date = DateTimeField(default=datetime.utcnow)
    title = StringField(required=True)
    content = StringField(required=True)

    @property
    def id(self):
        return str(self.pk)

    def to_dict(self):
        return {
            "_id": str(self.pk),
            "author": self.author,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title": self.title,
            "content": self.content,
        }
