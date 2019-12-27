#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import warnings
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)

from gthnk import create_app
app = create_app()

if 'IP' in app.config:
  app.run(host=app.config['IP'], port=app.config['PORT'])
else:
  app.run(port=app.config['PORT'])
