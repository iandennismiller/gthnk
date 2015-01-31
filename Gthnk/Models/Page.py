# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

from flask.ext.diamond.utils.mixins import CRUDMixin
from Gthnk import db
from wand.image import Image
from wand.color import Color


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
        with Image(blob=self.binary, resolution=150) as img:
            if img.format == "pdf":
                pass
            self.extension = img.format.lower()
            flattened = Image(background=Color("white"),
                height=img.height, width=img.width)
            flattened.composite(img, left=0, top=0)
            flattened.format = "jpeg"
            flattened.compression_quality = 50

            thumbnail = flattened.clone()
            thumbnail.transform(resize='150x200>')
            self.thumbnail = thumbnail.make_blob()

            preview = flattened.clone()
            preview.gaussian_blur(radius=1, sigma=0.5)
            preview.transform(resize='612x792>')
            self.preview = preview.make_blob()
        self.save()

    def filename(self):
        return '{0}-{1}.{2}'.format(self.day.date, self.sequence, self.extension)

    def cache_filename(self):
        return '{0}-{1}.{2}'.format(self.day.date, self.sequence, "jpg")

    def __repr__(self):
        if self.sequence is not None:
            return '<Page filename: %s-%d.pdf>' % (self.day.date, self.sequence)
        else:
            return '<Page filename: %s-xxx.pdf>' % (self.day.date)

    def __unicode__(self):
        return repr(self)
