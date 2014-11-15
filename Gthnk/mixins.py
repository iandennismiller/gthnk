# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from GT import db, app

# adapted from https://github.com/semirook/flask-kit/blob/master/base/models.py
class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def find(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        result = instance.save()
        app.logger.debug("create %r: %r" % (instance, result))
        return result

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()