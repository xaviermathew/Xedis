import logging
from pprint import pprint
import socket

from xedis import settings
from xedis.utils import deserialize

_LOG = logging.getLogger(__name__)


class XedisClient(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((settings.SERVER_HOST, settings.SERVER_PORT))

    @staticmethod
    def pprint(response):
        if response['status'] == 200:
            data = response['data']
            if isinstance(data, basestring):
                print '<OK>', data
            elif data is None:
                print '<OK>'
            else:
                pprint(data)
        else:
            print '<ERROR> %s' % response['error']

    def execute(self, cmd):
        self.sock.send(cmd)
        return self.sock.recv(settings.CLIENT_REQUEST_BUFFER)

    def exit(self):
        _LOG.info('Exiting')
        self.sock.close()

    def repl(self):
        while True:
            try:
                line = raw_input('xedis> ')
                if line:
                    if line == 'exit':
                        self.exit()
                        break
                    response = self.execute(line)
                    self.pprint(deserialize(response))
            except (KeyboardInterrupt, EOFError):
                self.exit()
                break
