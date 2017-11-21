#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import flask
import gthnk
from gthnk.adaptors.librarian import Librarian


def main():
    app = flask.Flask(__name__)
    app.config.from_envvar('SETTINGS')
    gthnk.db.init_app(app)
    with app.app_context():
        librarian = Librarian(app)
        librarian.rotate_buffers()
        # also export the journal for safe-keeping
        librarian.export_journal()

if __name__ == "__main__":
    main()
