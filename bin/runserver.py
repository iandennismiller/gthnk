#!/usr/bin/env python
# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import Gthnk, logging
app = Gthnk.create_app()
#logging.getLogger("gthnk").info("runserver.py starting")
app.run(port=app.config['PORT'])
