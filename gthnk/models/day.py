# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller
import StringIO
import datetime
import re

from PyPDF2 import PdfFileReader, PdfFileWriter
from flask.ext.diamond.utils.mixins import CRUDMixin
from sqlalchemy import desc
from sqlalchemy.ext.orderinglist import ordering_list
from wand.image import Image

from .. import db


class Day(db.Model, CRUDMixin):
    """
    A Day consists of the Entry objects that were created on that day.
    This is just a convenient way of referring to Entry objects in the database.
    This object is also capable of creating a string that is parsable by the JournalBuffer
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True)

    pages = db.relationship("Page", order_by="Page.sequence",
        collection_class=ordering_list('sequence', reorder_on_append=True),
        backref=db.backref("day"))

    def add_page(self, binary):
        from page import Page
        page = Page.create(day=self)
        page.set_image(binary=binary)
        self.pages.append(page)
        self.pages.reorder()
        db.session.commit()

    def attach(self, binary):
        # determine the format of the file
        binary_format = Image(blob=binary).format
        if binary_format == "PDF":
            # use PyPDF2 to read the stream
            pdf = PdfFileReader(StringIO.StringIO(binary))
            if pdf.getNumPages() > 1:  # if it is a multi-page PDF
                for pdf_page in pdf.pages:  # add the pages individually
                    output = PdfFileWriter()
                    output.addPage(pdf_page)

                    pdf_page_buf = StringIO.StringIO()
                    output.write(pdf_page_buf)
                    self.add_page(pdf_page_buf.getvalue())
            else:  # if it is just a single page PDF
                # then add the original bytestream
                self.add_page(binary)
        elif binary_format:
            self.add_page(binary)
        else:  # could not recognize file
            pass

    def render_pdf(self):
        outpdf = PdfFileWriter()
        for page in self.pages:
            if page.extension == "pdf":
                outpdf.addPage(PdfFileReader(StringIO.StringIO(page.binary)).getPage(0))
            else:
                img = Image(blob=page.binary, resolution=72)
                img.format = "jpg"
                img.format = "pdf"
                outpdf.addPage(PdfFileReader(StringIO.StringIO(img.make_blob())).getPage(0))

        pdf_page_buf = StringIO.StringIO()
        outpdf.write(pdf_page_buf)
        return pdf_page_buf.getvalue()

    def yesterday(self):
        return self.query.filter(Day.date < self.date).order_by(desc(Day.date)).first()

    def tomorrow(self):
        return self.query.filter(Day.date > self.date).order_by(Day.date).first()

    def render(self):
        from entry import Entry
        buf = datetime.datetime.strftime(self.date, "%Y-%m-%d")
        for entry in self.entries.order_by(Entry.timestamp).all():
            buf += unicode(entry)
        buf += "\n\n"
        return buf

    def render_markdown(self):
        buf = self.render()
        buf = re.sub(r'(\d\d\d\d-\d\d-\d\d)\n', '# \g<1>\n', buf)
        buf = re.sub(r'(\d\d\d\d)\n', '## \g<1>\n', buf)

        img_fmt = "[![{sequence}](../thumbnail/{attachment})](../attachment/{attachment})\n"

        if len(self.pages) > 0:
            buf += "# Attachments\n\n"
            for page in self.pages:
                buf += img_fmt.format(
                    sequence=page.sequence,
                    thumbnail=page.filename(extension="jpg"),
                    attachment=page.filename()
                )

        return buf

    def __repr__(self):
        return "<Day: {}>".format(self.date)

    def __unicode__(self):
        return repr(self)


def latest():
    return Day.query.order_by(desc(Day.date)).first()
