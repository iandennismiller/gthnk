from setuptools import setup

version = '0.2'

setup(version=version,
    name='gthnk',
    description="gthnk",
    packages=[
        "Gthnk",
        "Gthnk.Adaptors",
        "Gthnk.Models",
        "Gthnk.Views",
        "Gthnk.Views.Frontend",
        "Gthnk.Views.Administration",
    ],
    scripts=[
        "bin/runserver.py",
        "bin/manage.py",
        "bin/journal_rotate.py",
        "bin/journal_export.py",
        #"bin/journal_actions.py",
    ],
    long_description="""gthnk""",
    classifiers=[],
    include_package_data=True,
    keywords='',
    author='Ian Dennis Miller',
    author_email='ian@iandennismiller.com',
    url='http://www.iandennismiller.com',
    dependency_links=[
        'https://github.com/iandennismiller/Flask-Diamond/archive/0.1.9.tar.gz#egg=flask_diamond-0.1.9',
        'https://github.com/iandennismiller/mdx_journal/archive/0.1.tar.gz#egg=mdx_journal-0.1',
    ],
    install_requires=[
        ### app
        "flask_diamond==0.1.9",
        "mdx_linkify==0.5",
        "poodledo>=0.2",
        "mdx_journal==0.1",
        "Wand==0.3.9",
        "Flask-Cache==0.13.1",

        ### other flask niceness
        "pyScss==1.2.0.post3",
        "lxml==3.4.0",
        "requests==2.4.1",
        "cssselect==0.9.1",
    ],
    license='Proprietary',
    zip_safe=False,
)
