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
    packages=[
        "gthnk",
        "gthnk_server",
        "gthnk_integration",
    ],
    scripts=[
        "scripts/gthnk",
        "scripts/gthnk-7-to-8.py",
    ],
    long_description=read('../Readme.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Flask",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3.8",
        "Topic :: Database :: Front-Ends",
    ],
    include_package_data=True,
    keywords='',
    author=grep('__author__'),
    author_email=grep('__email__'),
    url=grep('__url__'),
    install_requires=[
        "six",
        "puremagic",
        "python-dotenv",
        "pytest",
        "rich",
        "requests",
    ],
    extras_require={
        "llm": [
            "llama-cpp-python==0.1.43",
            "chromadb==0.3.21",
        ],
        "dev": [
            "pdbpp",
            "GitPython",
            "Sphinx",
            "alabaster",
            "twine",
            "ipython",
            "watchdog",
            "pylint",
            "Flask-Testing",
            "rstcheck",
        ],
        "server": [
            "jinja2<3.1.0",
            "flask==1.1.2",
            "werkzeug==2.0.3",
            "Markdown<3.2",
            "itsdangerous==2.0.1",
            "flask-login",
            "Flask-WTF",
            "flask-markdown",
            "mdx-linkify==1.0",
            "mdx-journal>=0.1.4",
        ],
    },
    license='MIT',
    zip_safe=False,
)
