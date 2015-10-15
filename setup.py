# encoding: utf-8
from setuptools import setup
from mytor import version

setup(
    name='mytor',
    version=version,
    packages=['mytor'],
    install_requires=[
        'tornado>=4.1',
        'PyMySQL==0.6.7',
        'greenlet>=0.4.2',
    ],
    author=['snower', 'mosquito'],
    author_email=['sujian199@gmail.com', 'me@mosquito.su'],
    url='https://github.com/mosquito/mytor',
    license='MIT',
    keywords=[
        "tornado", "mysql"
    ],
    description='Tornado asynchronous MySQL Driver [fork of TorMysql]',
    long_description=open("README.rst").read(),
    zip_safe=False,
)
