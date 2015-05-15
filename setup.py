import os

from setuptools import setup
from setuptools import find_packages


def read(*paths):

    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='tmx',
    version='0.0.1',
    description='Handle tmx files',
    long_description='',
    url='https://github.com/jakub-szczepaniak/Tmx',
    license='MIT',
    author='Jakub Szczepaniak',
    author_email='szczepaniak.jkb@gmail.com',
    packages=find_packages(exclude=['test*']),
    classifiers=[
        'Development Status :: 1',
        'Intended Audience :: Developers',
        'Private :: Do Not Upload'],)
