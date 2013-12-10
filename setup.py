from setuptools import setup
import os, shutil

version = '0.1'

setup(version=version,
      name='greenthink-library',
      description = "greenthink-library",
      packages = ["GT"],
      scripts = [
            "bin/runserver.py",
            "bin/manage.py",
            "bin/journal_rotate.py",
            "bin/journal_get.sh",
            "bin/journal_delete.sh",
            "bin/journal_cron.sh",
            "bin/journal_actions.py",
      ],
      long_description="""greenthink-library""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      include_package_data = True,
      keywords='',
      author='Ian Dennis Miller',
      author_email='ian@iandennismiller.com',
      url='http://www.iandennismiller.com',
      install_requires = [
            ### application requirements

            "poodledo>=0.2",
            #"BeautifulSoup==3.2.1",
            #"html5lib>=0.95",
            #"requests==2.0.0",
            #"Whoosh==2.5.1",
            #"lxml==3.2.4",
            #"Unidecode==0.04.14",
            #"python-dateutil==2.2",

            ### development

            "Sphinx==1.1.3",
            "Fabric==1.8.0",
            "nose==1.2.1",
            "watchdog==0.6.0",
            "ipython>=0.13",
            "pylint==0.26.0",

            ### Flask Framework

            "Werkzeug==0.8.3",
            "Jinja2==2.6",
            "Flask==0.10.1",
            "Flask-Admin==1.0.6",
            "Flask-WTF==0.9.3",
            "Flask-Login==0.2.7",
            "Flask-Security==1.6.9",
            "Flask-Script==0.6.2",
            "Flask-Migrate==0.1.4",

            ### databases

            ### mongodb
            # "pymongo==2.6.3",
            # "Flask-MongoEngine>=0.1.3",
            ### sqlalchemy
            "SQLAlchemy==0.8.2",
            "Flask-SQLAlchemy>=1.0",
            "alembic==0.6.0",
      ],
      license='Proprietary',
      zip_safe=False,
)