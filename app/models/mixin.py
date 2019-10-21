from app import db


class DictMixin(db.Model):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
