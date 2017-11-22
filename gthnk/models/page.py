# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from flask_diamond.mixins.crud import CRUDMixin
from .. import db
from PIL import Image
from io import BytesIO


class Page(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    sequence = db.Column(db.Integer)
    binary = db.Column(db.Binary)
    title = db.Column(db.Unicode(1024))
    thumbnail = db.Column(db.Binary)
    preview = db.Column(db.Binary)
    extension = db.Column(db.String(32))

    def set_image(self, binary):
        self.binary = binary
        with Image.open(BytesIO(self.binary)) as img:
            self.extension = img.format.lower()

            # flatten image
            flattened = img.copy().convert("RGB")

            # create 150x200 thumbnail
            size = (150, 200)
            thumb = flattened.copy()
            thumb.thumbnail(size)
            thumb_buf = BytesIO()
            thumb.save(thumb_buf, "JPEG")
            self.thumbnail = thumb_buf.getvalue()

            # create preview
            size = (612, 792)
            preview = flattened.copy()
            preview.thumbnail(size)
            preview_buf = BytesIO()
            preview.save(preview_buf, "JPEG")
            self.preview = preview_buf.getvalue()

        # write to DB
        self.save()

    def filename(self, extension=None):
        if not extension:
            extension = self.extension
        return '{0}-{1}.{2}'.format(self.day.date, self.sequence, extension)

    def content_type(self):
        if self.extension == 'pdf':
            return 'application/pdf'
        elif self.extension == 'gif':
            return 'image/gif'
        elif self.extension == 'png':
            return 'image/png'
        elif self.extension == 'jpg':
            return 'image/jpeg'

    def __repr__(self):
        if self.sequence is not None:
            return '<Page filename: %s-%d.pdf>' % (self.day.date, self.sequence)
        else:
            return '<Page filename: %s-xxx.pdf>' % (self.day.date)

    def __unicode__(self):
        return repr(self)
