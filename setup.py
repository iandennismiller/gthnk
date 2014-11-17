from setuptools import setup
import os, shutil

version = '0.2'

setup(version=version,
      name='greenthink',
      description = "greenthink",
      packages = [
            "Gthnk",
            "Gthnk.Adaptors",
            "Gthnk.Models",
            "Gthnk.Views",
            "Gthnk.Views.Frontend",
            "Gthnk.Views.Administration",
            ],
      scripts = [
            "bin/runserver.py",
            "bin/manage.py",
            "bin/journal_rotate.py",
            #"bin/journal_actions.py",
      ],
      long_description="""greenthink-library""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      include_package_data = True,
      keywords='',
      author='Ian Dennis Miller',
      author_email='ian@iandennismiller.com',
      url='http://www.iandennismiller.com',
      dependency_links = [
            'https://github.com/iandennismiller/Flask-Diamond/archive/0.1.7.tar.gz#egg=flask_diamond-0.1.7',
            'https://github.com/iandennismiller/mdx_journal/archive/0.1.tar.gz#egg=mdx_journal-0.1',
            ],
      install_requires = [
            ### app
            "watchdog==0.8.2",
            #"flask_diamond==0.1.7",
            "mdx_linkify==0.5",
            #"Markdown>=2.3.1",
            "poodledo>=0.2",
            "mdx_journal==0.1",

            ### other flask niceness

            "pyScss==1.2.0.post3",
            "wheel==0.24.0",
            "Flask-RESTful==0.2.12",
            "lxml==3.4.0",
            "requests==2.4.1",
            "cssselect==0.9.1",
            "Flask-DbShell==1.0",
            #"python-dateutil==2.2",


            ### databases
            "SQLAlchemy==0.9.3",
            "Flask-SQLAlchemy>=1.0",
            "SQLAlchemy-Utils==0.24.1",
      ],
      license='Proprietary',
      zip_safe=False,
)
