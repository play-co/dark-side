#!/usr/bin/python

from distutils.core import setup


setup(name='dark-side',
      version='1.0.1',   
      description='response comparing proxy server', 
      requires=['gevent','requests','json_tools'],
      author='mark neyer',
      scripts=['darkside.py'])
