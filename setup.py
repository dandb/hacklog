import os
import sys
from setuptools import setup, Command

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

#from distutils.core import setup, Command
# you can also import from setuptools

#FIXME:  mockito really should not be there, however it does not get installed as test dependecy when added to 'tests_require'
install_requires = [
  'twisted',
  'SQLAlchemy',
  'mockito',
  ]

tests_require = [
  'pytest',
  'mockito',
  ]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hacklog",
    version = "0.0.5",
    author = "DandB Hackweek Team - Hackling Ouliers",
    author_email = "hacklog@dandb.com",
    description = ("Syslog server for detection of compromised user accounts by"
                                   "applying statical analysis to server authentication logs"),
    license = "GPLv3",
    keywords = "hacking security logs syslog outliers statistical analysis",
    url = "https://github.com/dandb/hacklog",
    packages=['hacklog'],
    install_requires = install_requires,
    tests_require = tests_require,
    extras_require={'test': tests_require},
    long_description=read('README.md') + '\n\n' + read('CHANGES'),
    test_suite = 'tests',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Internet :: Log Analysis",
        "Topic :: System :: Logging",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
)

