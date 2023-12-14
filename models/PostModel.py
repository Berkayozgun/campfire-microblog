from bson import ObjectId


class PostModel(object):
    def __init__(self, user_id, title, content, date, image):
        self._id = ObjectId()
        self.user_id = user_id
        self.title = title
        self.content = content
        self.date = date
        self.image = image

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        return {
            "_id": str(self.id),
            "user_id": str(self.user_id),
            "title": self.title,
            "content": self.content,
            "date": self.date,
            "image": self.image,
        }
