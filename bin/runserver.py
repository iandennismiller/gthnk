#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gthnk (c) 2014-2016 Ian Dennis Miller

from Gthnk import create_app
app = create_app()
app.run(port=app.config['PORT'])
