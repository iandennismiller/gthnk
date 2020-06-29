# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import puremagic
import re
from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileWriter
from flask_diamond.mixins.crud import CRUDMixin
from sqlalchemy import desc
from sqlalchemy.ext.orderinglist import ordering_list
from PIL import Image
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
        from .page import Page
        page = Page.create(day=self)
        page.set_image(binary=binary)
        self.pages.append(page)
        self.pages.reorder()
        db.session.commit()
        return(page)

    def attach(self, binary):
        # determine the format of the file
        ext = puremagic.from_string(binary)

        page = None

        # if the attachment is a PDF
        if ext == ".pdf":
            # use PyPDF2 to read the stream
            pdf = PdfFileReader(BytesIO(binary))
            # if it is a multi-page PDF
            if pdf.getNumPages() > 1:
                # add the pages individually
                for pdf_page in pdf.pages:
                    output = PdfFileWriter()
                    output.addPage(pdf_page)

                    pdf_page_buf = BytesIO()
                    output.write(pdf_page_buf)
                    page = self.add_page(pdf_page_buf.getvalue())
            # if it is just a single page PDF
            else:
                # then add the original bytestream
                page = self.add_page(binary)
        # if the attachment is a recognized image
        elif ext in [".png", ".jfif", ".gif", ".jpeg", ".jpg"]:
            page = self.add_page(binary)
        # could not recognize file
        else:
            pass

        if page:
            return(page)

    def render_pdf(self):
        outpdf = PdfFileWriter()
        for page in self.pages:
            if page.extension == "pdf":
                # the page is already a PDF so append directly
                outpdf.addPage(PdfFileReader(BytesIO(page.binary)).getPage(0))
            else:
                # otherwise, the page is an image that needs to be converted to PDF first
                buf = BytesIO()
                img = Image.open(BytesIO(page.binary))
                img.convert("RGB").save(buf, format="pdf")
                # once image is PDF, it can be appended
                outpdf.addPage(PdfFileReader(buf).getPage(0))

        pdf_page_buf = BytesIO()
        outpdf.write(pdf_page_buf)
        return(pdf_page_buf.getvalue())

    def yesterday(self):
        return(self.query.filter(Day.date < self.date).order_by(desc(Day.date)).first())

    def tomorrow(self):
        return(self.query.filter(Day.date > self.date).order_by(Day.date).first())

    def render(self):
        from .entry import Entry
        buf = self.date.strftime("%Y-%m-%d")
        for entry in self.entries.order_by(Entry.timestamp).all():
            buf += str(entry)
        buf += "\n\n"
        return(buf)

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
        return("<Day: {}>".format(self.date))

    def __unicode__(self):
        return(self.render())

    def __str__(self):
        return(self.__unicode__())


def latest():
    return(Day.query.order_by(desc(Day.date)).first())
