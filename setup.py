#!/usr/bin/python

from distutils.core import setup


setup(name='dark-side',
      version='1.0.5',   
      description='response comparing proxy server', 
      author='mark neyer',
      url='https://github.com/gameclosure/dark-side',
      install_requires=['gevent','requests','json_tools','webob'],
      scripts=['darkside.py'])
