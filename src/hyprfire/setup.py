#!/usr/bin/env python
from setuptools import setup

setup(
    name='hyprfire',
    version='1.0',
    packages=['.','hyprfire', 'hyprfire_app', 'hyprfire_app/new_scripts', 'hyprfire_app/old_scripts',
              'hyprfire_app/scripts', 'hyprfire_app/migrations' , 'logs', 'pcaps'],
    url='',
    license='no license as of now',
    author='yo',
    author_email='no email',
    description='This is hyprfire.',
    install_requires=[
        "hyprfire",
        "asgiref>=3.2.7",
        "Django==3.0.5",
        "plotly>=4.6.0",
        "pytz>=2019.3",
        "retrying>=1.3.3",
        "six>=1.14.0",
        "sqlparse>=0.3.1",
        "wireshark>=2.6.10",
    ],
    include_package_data=True,
)
