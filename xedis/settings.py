import logging

DATA_DUMP_LOCATION = '/tmp/xedis.dump'
DATA_DUMP_INTERVAL = 30
SERVER_HOST = 'localhost'
SERVER_PORT = 6379
SERVER_REQUEST_BUFFER = 8192
CLIENT_REQUEST_BUFFER = 8192

logging.basicConfig(level=logging.DEBUG)
