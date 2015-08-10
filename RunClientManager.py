__author__ = 'liuhui'

from multiprocessing.managers import SyncManager

IP = '127.0.0.1'
PORTNUM = 5020
AUTHKEY = b'authkey'

def make_client_manger():
    # print('step1')
    class MyServerManager(SyncManager): pass
    # print('step2')
    MyServerManager.register('get_lex_dic')
    # print('step3')
    manager = MyServerManager(address=(IP, PORTNUM),authkey=AUTHKEY)
    # print('step4')
    manager.connect()

    print("Client connected to %s:%s" %(IP, PORTNUM))
    return manager