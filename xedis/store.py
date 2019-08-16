import logging
import pickle
from threading import Timer

from xedis import settings

_LOG = logging.getLogger(__name__)
STORE = {}


def persist():
    _LOG.debug('Why Mr. Anderson? Why? Why do u persist?')
    with open(settings.DATA_DUMP_LOCATION, 'w') as f:
        pickle.dump(STORE, f)


def load_persisted():
    with open(settings.DATA_DUMP_LOCATION) as f:
        data = pickle.load(f)
        _LOG.info('recovered %s items from dump', len(data))
        STORE.update(data)


def start_persisting():
    def new_thread():
        def f():
            persist()
            new_thread()
        t = Timer(settings.DATA_DUMP_INTERVAL, f)
        t.setDaemon(True)
        t.start()

    new_thread()
