#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import glob
# import logging

import sys
sys.path.insert(0, '.')

import os
import flask
import Gthnk
import Gthnk.Adaptors.JournalBuffer


def main():
    app = flask.Flask(__name__)
    app.config.from_envvar('SETTINGS')
    Gthnk.db.init_app(app)

    with app.app_context():
        app.logger.info("start")

        # create export path if necessary
        if not os.path.exists(app.config["EXPORT_PATH"]):
            os.makedirs(app.config["EXPORT_PATH"])
            os.makedirs(os.path.join(app.config["EXPORT_PATH"], "day"))
            os.makedirs(os.path.join(app.config["EXPORT_PATH"], "attachment"))

        for day in Gthnk.Models.Day.query.all():
            app.logger.info(day)
            output_filename = os.path.join(app.config["EXPORT_PATH"], "day",
                "{0}.txt".format(day.date))
            with open(output_filename, "w") as f:
                f.write(day.render())

        for page in Gthnk.Models.Page.query.all():
            app.logger.info(page)
            output_filename = os.path.join(app.config["EXPORT_PATH"], "attachment",
                page.filename())
            with open(output_filename, "w") as f:
                f.write(page.binary)

        app.logger.info("finish")

        # now reset the file size to 0.
        #with open(filename, "w"):
        #    pass


if __name__ == "__main__":
    main()
