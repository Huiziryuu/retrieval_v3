__author__ = 'liuhui'

import RetrievalHash
from multiprocessing.managers import SyncManager

HOST = '127.0.0.1'
PORTNUM = 5020
AUTHKEY = b'authkey'

def make_server_manager():

    class MyManager(SyncManager): pass

    lex_dic = RetrievalHash.RetrievalHash()

    MyManager.register('get_lex_dic',callable=lambda : lex_dic)

    manager = MyManager(address=('', PORTNUM),authkey=AUTHKEY)
    s = manager.get_server()
    s.serve_forever()
    # s.shutdown()

if __name__ == '__main__':
    make_server_manager()

