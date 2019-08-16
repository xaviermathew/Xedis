import asyncore
import logging
import socket

from xedis import settings
from xedis.parser import parse
from xedis.store import start_persisting, load_persisted
from xedis.utils import serialize

_LOG = logging.getLogger(__name__)


class RequestHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        cmd = self.recv(settings.SERVER_REQUEST_BUFFER)
        if not cmd:
            _LOG.info('remote:%s closing connection', self.addr)
            return

        _LOG.info('remote:%s cmd:[%s]', self.addr, cmd)
        try:
            response = parse(cmd)
        except Exception as ex:
            self.send(serialize(ex))
        else:
            self.send(serialize(response))


class XedisServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        _LOG.info('listening on:%s', self.addr)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            _LOG.info('remote:%s incoming connection', addr)
            RequestHandler(sock)


def start_serving(recover=False):
    if recover:
        load_persisted()
    start_persisting()
    XedisServer(settings.SERVER_HOST, settings.SERVER_PORT)
    asyncore.loop()
