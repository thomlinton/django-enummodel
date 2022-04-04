from setuptools import setup, find_packages
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-enummodel",
    version = "1.0.0.dev0",
    author = "Thom Linton",
    author_email = "thom.linton@gmail.com",
    description = "A Django application to bridge the gap between using enumerations and having fully-specified, normalized data models.",
    license = "BSD",
    keywords = "",
    url = "http://github.com/thomlinton/django-enummodel",
    install_requires=['Django~=3.2'],
    packages=find_packages(),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
    package_data={
    },
)
