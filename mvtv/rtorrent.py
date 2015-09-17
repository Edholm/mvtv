# Interface with rtorrent through xmlrpc.

import sys
import xmlrpc.client


class RTorrent(object):
    def __init__(self):
        self.url = "http://arch.edholm.it"
        self.proxy = xmlrpc.client.ServerProxy(self.url)
        self.list_cache = None

    def list(self):
        if not self.list_cache:
            self.list_cache = self.proxy.d.multicall('main', 'd.get_name=', 'd.get_hash=',
                                                     'd.base_path=')
        return self.list_cache

    def close(self, torrent):
        if not self.verify(torrent):
            return
        self.proxy.d.close(torrent)

    def start(self, torrent):
        if not self.verify(torrent):
            return
        self.proxy.d.resume(torrent)

    def set_base_path(self, torrent, new_path):
        if not self.verify(torrent):
            return
        self.proxy.d.set_directory_base(torrent, new_path)

    def search_by_name(self, name):
        return self._search_by_index(name, 0)

    def search_by_path(self, path):
        return self._search_by_index(path, 2)

    def _search_by_index(self, query, index):
        all = self.list()
        return next((x for x in all if query in x[index]), None)

    def exists(self, torrent):
        ''' torrent should be a hash '''
        if not self._is_hash(torrent):
            return False

        hash = None
        try:
            hash = self.proxy.d.get_hash(torrent)
        except xmlrpc.client.Fault:
            return False
        return hash == torrent.upper()

    def info(self, torrent):
        print('Not yet implemented', file=sys.stderr)
        pass

    def _is_hash(self, torrent):
        if type(torrent) != str or len(torrent) != 40:
            return False

        import re
        p = re.compile("[a-zA-Z0-9]{40}")
        return p.match(torrent) is not None

    def verify(self, torrent):
        if not self._is_hash(torrent):
            print('"' + torrent + '" is not a valid hash', file=sys.stderr)
            return False
        return True
