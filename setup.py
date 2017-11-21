# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from setuptools import setup, find_packages
import os
import re


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


file_text = read(fpath('gthnk/__meta__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    version=grep('__version__'),
    name='gthnk',
    description="gthnk is a personal knowledge management system",
    packages=find_packages(),
    scripts=[
        "bin/runserver.py",
        "bin/manage.py",
        "bin/integration.py",
        "bin/gthnk",
        "bin/gthnk.cmd",
        "bin/gthnk-rotate.py",
        "bin/gthnk-rotate.cmd",
    ],
    long_description=read('Readme.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Flask",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.7",
        "Topic :: Database :: Front-Ends",
    ],
    include_package_data=True,
    keywords='',
    author=grep('__author__'),
    author_email=grep('__email__'),
    url=grep('__url__'),
    install_requires=read('requirements.txt'),
    license='MIT',
    zip_safe=False,
)
