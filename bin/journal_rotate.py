#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import Gthnk
import Gthnk.Adaptors.JournalBuffer
from Gthnk.Librarian import Librarian


def main():
    app = flask.Flask(__name__)
    app.config.from_envvar('SETTINGS')
    Gthnk.db.init_app(app)
    with app.app_context():
        librarian = Librarian(app)
        librarian.rotate_buffers()

if __name__ == "__main__":
    main()
