"""
This script runs the Auditoria application using a development server.
"""

from os import environ
from Auditoria import app
#from flask import Flask
import random

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.secret_key = ''.join(list(map(lambda x:random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'),[0]*32)))

    app.debug = True
    app.run(HOST, PORT, threaded=True)

    #app = Flask(__name__)

